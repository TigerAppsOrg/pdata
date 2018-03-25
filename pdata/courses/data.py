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

from pdata.utils import bulk_upsert_item
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
    _update_subject_data(subject_info, term)

def _update_subject_data(data: dict, term: models.Semester) -> None:
  '''
  Update a subject's data, if present, with new information. If not present,
  the relevant objects in the database are created.

  :param data: subject data
  '''
  dept = data['code']

  created_courses = []

  for course_info in data['courses']:
    num_tuple = _catalog_num_to_tuple(course_info['catalog_number'])

    course, created = bulk_upsert_item(
      models.Course,
      department=dept,
      number=num_tuple[0],
      letter=num_tuple[1],
      defaults={
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

    if created:
      created_courses.append(course)

  models.Course.bulk_create(created_courses)

def _catalog_num_to_tuple(catalog_number: str) -> typing.Tuple[int, str]:
  '''
  Convert a Registrar catalog number to a tuple of (number, letter). For
  example, '200' is converted to (200, '') and '200A' is converted to
  (200, 'A').

  :param catalog_number: number to convert

  :return: tuple of (number, letter)
  '''
  return (int(catalog_number[:3]), catalog_number[3:])
