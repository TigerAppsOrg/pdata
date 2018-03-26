# pdata/courses/data.py
# pdata
# Author: Rushy Panchal
# Date: March 20th, 2018
# Description: Data-fetching functions and task definitions for courses
#              dataset.

import typing

import logging
import urllib.request
import json

from pdata.utils import bulk_upsert
from . import models

BASE_URL = 'https://etcweb.princeton.edu/webfeeds/courseofferings/?term={term}&subject=all&fmt=json'
LOGGER = logging.getLogger('pdata.courses')

def fetch_term_data(term: typing.Union[str, int] = 'current')
    -> typing.Optional[dict]:
  '''
  Fetch the data associated with the given term.

  :param term: term to obtain data for

  :return: data for given term
  '''
  url = BASE_URL.format(term=term)
  try:
    req = urllib.request.urlopen(url)
  except urllib.error.URLError as e:
    LOGGER.error('Could not fetch term data: %s' % str(e))
    return None
  else:
    data = req.read()
    return json.parse(data)

@transaction.atomic
def update_term_data(data: dict) -> None:
  '''
  Update a term's data, if present, with new information. If not present, the
  data is created. This is performed atomically.

  :param data: term data retrieved from webfeeds
  '''
  # Updates are performed in the following order. All updates are performed
  # in bulk, as possible.
  # 
  #   1. Update the term information. This is independent of any other objects.
  #   2. Update all of the instructors. Instructors do not depend on any other
  #      objects, but offerings depend on instructors.
  #   3. Update all of the courses. Courses do not depend on any other object.
  #      The updates are done in-bulk for all departments (at once). This is
  #      done at the same time as the above.
  #   4. Update all of the crosslistings for each course. This is done
  #      all at once, not *per-course*. In other words, due to the
  #      bulk-updating of courses, all courses must be updated before any
  #      of the crosslistings can be updated.
  #   5. Update all of the offerings for each course. Similar to the above,
  #      the offerings are updated all at once and not *per-course*. The
  #      instructor-to-offering mapping is also performed here.

  term_info = data['term']

  # 1.
  term, _ = models.Semester.objects.update_or_create(
    term_id=term_info['code'],
    defaults={
      'term': (models.Semester.TERM_FALL if 'F' in term_info['suffix']
        else models.Semester.TERM_SPRING)
      'year': int(term_info['suffix'][1:]),
      'start_date': term_info['start_date'],
      'end_date': term_info['end_date']
      })

  # 2. and 3.
  _update_instructors_and_courses(term_info['subjects'])

  # 4.
  _update_subject_crosslistings(term_info['subjects'])

  # 5.
  _update_subject_offerings(term_info['subjects'], term)

def _get_course_pk_map(**kwargs) -> typing.Dict[str, int]:
  '''
  Get a map between course catalog numbers and their primary keys. kwargs can
  be used to pass in a filter to the query.

  :param kwargs: filter parameters for query

  :return: map of catalog numbers to primary keys
  '''
  courses = (models.Course.objects
    .filter(**kwargs)
    .values_list('number', 'letter', 'id'))
  return {('%d%s' % (num, ltr)): pk for (num, ltr, pk) in courses}

def _update_instructors_and_courses(subject_data: typing.List[dict]) -> None:
  '''
  Update all of the instructors and courses, for all departments.

  :param subject_data: all subject data
  '''
  expected_emplid = set()
  expected_employees = []
  expected_courses = []

  for subject_info in subject_data:
    dept = subject_info['code']

    for course_info in subject_info['courses']:
      num_tuple = _catalog_num_to_tuple(course_info['catalog_number'])
      expected_courses.append({
        'department': dept,
        'number': num_tuple[0],
        'letter': num_tuple[1],
        'track': (models.Course.TRACK_UNDERGRAD
            if course_info['detail']['track'] == 'UGRAD'
            else models.Course.TRACK_GRAD),
        'title': course_info['title'],
        'description': course_info['detail']['description'],
        # TODO: these are not provided by the webfeed...
        'distribution_area': '',
        'pdf_allowed': False,
        'audit_allowed': False,
        })

      for instructor_info in course_info['instructors']:
        if instructor_info['emplid'] not in expected_emplid:
          full_name = '%s %s' % (instructor['first_name'],
            instructor['last_name'])
          expected_employees.append({
            'employee_id': instructor['emplid'],
            'first_name': instructor['first_name'],
            'last_name': instructor['last_name'],
            'full_name': (instructor['full_name']
              if full_name != instructor['full_name'] else None),
            })
          expected_emplid.add(instructor_info['emplid'])

  bulk_upsert(
    models.Instructor.objects.all(),
    lambda d: hash(d['employee_id']),
    expected_employees,
    )

  bulk_upsert(
    models.Course.objects.all(),
    lambda d: hash('%s%d%s' % (d['department'], d['number'], d['letter'])),
    expected_courses)

def _update_subject_crosslistings(subject_data: typing.List[dict]) -> None:
  '''
  Update all subjects' crosslistings for all of their courses.

  :param subject_data: all subject data
  '''
  pk_map = _get_course_pk_map()
  expected = []

  for subject_info in subject_data:
    dept = subject_info['code']

    for course_info in subject_info['courses']:
      course_pk = pk_map[course_info['catalog_number']]

      for crosslisting_info in course_info['crosslistings']:
        num_tuple = _catalog_num_to_tuple(crosslisting_info['catalog_number'])

        expected.append({
          'department': crosslisting_info['subject'],
          'number': num_tuple[0],
          'letter': num_tuple[1],
          'course_id': course_pk,
          })

  bulk_upsert(
    models.CrossListing.objects.all(),
    lambda d: hash('%s%d%s-%d' % (
      d['department'], d['number'], d['letter'], d['course_id'])),
    expected
    )

def _update_subject_offerings(
  subject_data: typing.List[dict],
  semester: models.Semester)
  -> None:
  '''
  Update all subjects' offerings for all of the courses in that subject. This
  includes registering the many-to-many relationship between instructors and
  offerings.

  :param subject_data: all subject data
  '''
  pk_map = _get_course_pk_map()
  expected_offerings = []

  for subject_info in subject_data:
    dept = subject_info['code']

    for course_info in subject_info['courses']:
      course_pk = pk_map[course_info['catalog_number']]

      if len(course_info['classes']):
        # Assume that all of the start_date and end_date for each class is the
        # same. So, choose an arbitrary class to obtain that data from.
        arbitrary_class = course_info['classes'][0]

        expected_offerings.append({
          'registrar_guid': course_info['guid'],
          'course': course_pk,
          'semester': semester,
          'start_date': arbitrary_class['schedule']['start_date'],
          'end_date': arbitrary_class['schedule']['end_date'],
          })

  bulk_upsert(
    models.Offering.objects.all(),
    lambda d: hash('%s%d%s-%d' % (
      d['department'], d['number'], d['letter'], d['course_id'])),
    expected_offerings
    )

  # Create all of the m2m relationships between courses and instructors.
  instructor_pk_map = {emplid: pk for (emplid, pk) in
    models.Instructor.objects.all().values_list('employee_id', 'id')}
  offering_pk_map = {guid: pk for (guid, pk) in
    models.Offering.objects.all().values_list('registrar_guid', 'id')}
  expected_instructor_m2m = []

  for subject_info in subject_data:
    for course_info in subject_info['courses']:
      if len(course_info['classes']):
        offering_pk = offering_pk_map[course_info['guid']]

        for instructor_info in course_info['instructors']:
          expected_instructor_m2m.append({
            'instructor_id': instructor_pk_map[instructor_info['emplid']],
            'offering_id': offering_pk,
            })

  m2m_model = models.Offering.instructors.through
  bulk_upsert(
    m2m_model.objects.all(),
    lambda d: hash('%d-%d' % (d['instructor_id'], d['offering-id'])),
    expected_instructor_m2m
    )

def _catalog_num_to_tuple(catalog_number: str) -> typing.Tuple[int, str]:
  '''
  Convert a Registrar catalog number to a tuple of (number, letter). For
  example, '200' is converted to (200, '') and '200A' is converted to
  (200, 'A').

  :param catalog_number: number to convert

  :return: tuple of (number, letter)
  '''
  return (int(catalog_number[:3]), catalog_number[3:])
