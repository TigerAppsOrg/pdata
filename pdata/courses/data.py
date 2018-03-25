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
  data is created.

  :param data: term data retrieved from webfeeds
  '''
  term_info = data['term']

  term, _ = models.Semester.objects.update_or_create(
    term_id=term_info['code'],
    defaults={
      'term': (models.Semester.TERM_FALL if 'F' in term_info['suffix']
        else models.Semester.TERM_SPRING)
      'year': int(term_info['suffix'][1:]),
      'start_date': term_info['start_date'],
      'end_date': term_info['end_date']
      })

  for subject_info in term_info['subjects']:
    _update_subject_data(subject_info)

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

def _update_subject_data(data: dict) -> None:
  '''
  Update a subject's data, if present, with new information. If not present,
  the relevant objects in the database are created.

  :param data: subject data
  '''
  dept = data['code']

  expected = []
  for course_info in data['courses']:
    num_tuple = _catalog_num_to_tuple(course_info['catalog_number'])

    expected.append({
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

  bulk_upsert(
    models.Course.objects.filter(department=dept),
    lambda d: hash('%s%d%s' % (d['department'], d['number'], d['letter'])),
    expected)

  _update_subject_crosslistings(data)

def _update_subject_crosslistings(data: dict) -> None:
  '''
  Update a subject's crosslistings for all of its courses.

  :param data: subject data
  '''
  dept = data['code']
  pk_map = _get_course_pk_map(department=dept)
  expected = []

  for course_info in data['courses']:
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

def _catalog_num_to_tuple(catalog_number: str) -> typing.Tuple[int, str]:
  '''
  Convert a Registrar catalog number to a tuple of (number, letter). For
  example, '200' is converted to (200, '') and '200A' is converted to
  (200, 'A').

  :param catalog_number: number to convert

  :return: tuple of (number, letter)
  '''
  return (int(catalog_number[:3]), catalog_number[3:])
