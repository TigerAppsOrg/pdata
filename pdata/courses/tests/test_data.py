# pdata/courses/tests/test_data.py
# pdata
# Author: Rushy Panchal
# Date: March 28th, 2018
# Description: Test data fetching/updating utilities.

import typing
import json
import os
import datetime
import itertools

from django.test import TestCase, SimpleTestCase

from courses import models, data

class ModelAssertions(object):
  '''
  Contains assertion functions for checking the equality of two model objects.
  These assertions do not check foreign-key relationships.
  '''
  def course_with_id(self, course: str) -> models.Course:
    '''
    Retrieve the course with the given identification string. The string is in
    the format [dept][number][letter].

    :param course: identification string for course

    :return: course object, if found
    '''
    dept = course[:3].upper()
    num = int(course[3:6])
    letter = course[6:7]

    return models.Course.objects.get(
      department=dept, number=num, letter=letter)

  def assertSemesterEqual(self,
      s1: models.Semester, s2: models.Semester) -> None:
    '''Assert that two semesters are equal.'''
    self.assertEqual(s1.term, s2.term)
    self.assertEqual(s1.year, s2.year)
    self.assertEqual(s1.start_date, s2.start_date)
    self.assertEqual(s1.end_date, s2.end_date)
    self.assertEqual(s1.term_id, s2.term_id)

  def assertCourseEqual(self,
      c1: models.Course, c2: models.Course) -> None:
    '''Assert that two courses are equal.'''
    self.assertEqual(c1.title, c2.title)
    self.assertEqual(c1.description, c2.description)
    self.assertEqual(c1.distribution_area, c2.distribution_area)
    self.assertEqual(c1.department, c2.department)
    self.assertEqual(c1.number, c2.number)
    self.assertEqual(c1.letter, c2.letter)
    self.assertEqual(c1.track, c2.track)
    self.assertEqual(c1.pdf_allowed, c2.pdf_allowed)
    self.assertEqual(c1.audit_allowed, c2.audit_allowed)

  def assertCrossListingEqual(self,
      cl1: models.CrossListing, cl2: models.CrossListing) -> None:
    '''Assert that two crosslistings are equal.'''
    self.assertEqual(cl1.department, cl2.department)
    self.assertEqual(cl1.number, cl2.number)
    self.assertEqual(cl1.letter, cl2.letter)
    self.assertEqual(cl1.course_id, cl2.course_id)

  def assertInstructorEqual(self,
      i1: models.Instructor, i2: models.Instructor) -> None:
    '''Assert that two instructors are equal.'''
    self.assertEqual(i1.first_name, i2.first_name)
    self.assertEqual(i1.last_name, i2.last_name)
    self.assertEqual(i1.full_name, i2.full_name)
    self.assertEqual(i1.employee_id, i2.employee_id)

  def assertOfferingEqual(self,
      o1: models.Offering, o2: models.Offering) -> None:
    '''Assert that two offerings are equal.'''
    self.assertEqual(o1.registrar_guid, o2.registrar_guid)
    self.assertEqual(o1.start_date, o2.start_date)
    self.assertEqual(o1.end_date, o2.end_date)
    self.assertEqual(o1.course_id, o2.course_id)
    self.assertEqual(o1.semester_id, o2.semester_id)

  def assertSectionEqual(self,
      s1: models.Section, s2: models.Section) -> None:
    '''Assert that two sections are equal.'''
    self.assertEqual(s1.number, s2.number)
    self.assertEqual(s1.section_id, s2.section_id)
    self.assertEqual(s1.status, s2.status)
    self.assertEqual(s1.capacity, s2.capacity)
    self.assertEqual(s1.enrollment, s2.enrollment)
    self.assertEqual(s1.offering_id, s2.offering_id)

  def assertMeetingEqual(self,
      m1: models.Meeting, m2: models.Meeting) -> None:
    '''Assert that two meetings are equal.'''
    self.assertEqual(m1.building, m2.building)
    self.assertEqual(m1.room, m2.room)
    self.assertEqual(m1.number, m2.number)
    self.assertEqual(m1.start_time, m2.start_time)
    self.assertEqual(m1.end_time, m2.end_time)
    self.assertEqual(m1.day, m2.day)
    self.assertEqual(m1.section_id, m2.section_id)

class TestUpdateTermData(TestCase, ModelAssertions):
  '''
  Test the update_term_data function for updating a term's data dynamically.
  '''
  DATA_PATH = os.path.dirname(os.path.realpath(__file__))

  def assertDatabaseState(self):
    '''
    Assert that the database is in the expected state.
    '''
    self.assertEqual(models.Semester.objects.count(), 1)
    sem = models.Semester.objects.get()

    self.assertSemesterEqual(sem, EXPECTED_OBJECTS['semester'])

    # Verify all courses exist.
    self.assertEqual(models.Course.objects.count(), 5)

    expected_courses = sorted(
      EXPECTED_OBJECTS['courses'].values(), key=lambda x: x.number)
    for index, c in enumerate(models.Course.objects.order_by('number')):
      self.assertCourseEqual(c, expected_courses[index])

    # Verify all crosslistings.
    self.assertEqual(models.CrossListing.objects.count(), 6)

    for course_id, clxs in EXPECTED_OBJECTS['crosslistings'].items():
      course = self.course_with_id(course_id)
      cl_existing = (models.CrossListing.objects
        .filter(course=course)
        .order_by('department'))

      clxs = sorted(clxs, key=lambda x: x.department)
      for cl in clxs:
        cl.course_id = course.pk

      for index, c in enumerate(cl_existing):
        self.assertCrossListingEqual(c, clxs[index])

    # Verify all instructors.
    self.assertEqual(models.Instructor.objects.count(), 6)

    instr_expected = sorted(
      EXPECTED_OBJECTS['instructors'].values(), key=lambda x: x.employee_id)
    instr_query = models.Instructor.objects.order_by('employee_id')
    for index, instr in enumerate(instr_query):
      self.assertInstructorEqual(instr, instr_expected[index])

    # Verify all offerings.
    self.assertEqual(models.Offering.objects.count(), 5)

    for course_id, expected_offering in EXPECTED_OBJECTS['offerings'].items():
      course = self.course_with_id(course_id)
      existing_offering = models.Offering.objects.get(
        course=course, semester=sem)
      expected_offering.course_id = course.pk
      expected_offering.semester_id = sem.pk

      self.assertOfferingEqual(existing_offering, expected_offering)

    # Verify instructor-offering mapping.
    instr_offer_model = models.Offering.instructor.through
    self.assertEqual(instr_offer_model.objects.count(), 8)

    for course_id, instrs in EXPECTED_OBJECTS['offering-instructors'].items():
      course = self.course_with_id(course_id)

      expected_emplid = sorted(
        [EXPECTED_OBJECTS['instructors'][x].employee_id for x in instrs])
      existing_instr_pks = (instr_offer_model.objects
        .filter(offering__course_id=course.pk, offering__semester=sem)
        .order_by('instructor__employee_id')
        .values_list('instructor__employee_id', flat=True))

      self.assertEqual(list(existing_instr_pks), list(expected_emplid))

    # Verify all sections.
    self.assertEqual(models.Section.objects.count(), 7)

    for course_id, sections in EXPECTED_OBJECTS['sections'].items():
      course = self.course_with_id(course_id)

      expected_sections = sorted(sections.values(), key=lambda x: x.section_id)
      existing_sections = (models.Section.objects.filter(
          offering__course_id=course.pk,
          offering__semester=sem)
        .order_by('section_id'))

      for index, existing_section in enumerate(existing_sections):
        expected_section = expected_sections[index]
        expected_section.offering_id = existing_section.offering_id
        self.assertSectionEqual(existing_section, expected_section)

    # Verify all meetings.
    self.assertEqual(models.Meeting.objects.count(), 13)

    for course_id, section_meetings in EXPECTED_OBJECTS['meetings'].items():
      course = self.course_with_id(course_id)

      expected_meetings = sorted(
        # First, sorted by section_id
        itertools.chain.from_iterable(
          map(
            lambda x: x[1],
            sorted(section_meetings.items(), key=lambda x: x[0]))),
        # Now, sorted by number
        key=lambda x: x.number,
        )
      existing_meetings = (models.Meeting.objects.filter(
          section__offering__course_id=course.pk,
          section__offering__semester=sem
        ).order_by('section__section_id', 'number'))

      for index, existing_meeting in enumerate(existing_meetings):
        expected_meeting = expected_meetings[index]
        expected_meeting.section_id = existing_meeting.section_id
        self.assertMeetingEqual(existing_meeting, expected_meeting)

  def test_update_term_data(self):
    '''
    update_term_data with an empty database should add the values to the
    database.
    '''
    with open(os.path.join(self.DATA_PATH, 'example_data.json')) as f:
      json_data = json.load(f)

    data.update_term_data(json_data)
    self.assertDatabaseState()    

EXPECTED_OBJECTS = {
  'semester': models.Semester(
    term=models.Semester.TERM_SPRING,
    year=2018,
    start_date=datetime.date(2018, 2, 5),
    end_date=datetime.date(2018, 6, 5),
    term_id=1184,
    ),
  'courses': {
    'ast401': models.Course(
      department='AST',
      number=401,
      title='Cosmology',
      description='A general review of extragalactic astronomy and cosmology.  Topics include the properties and nature of galaxies, clusters of galaxies, superclusters, the large-scale structure of the universe, evidence for the existence of Dark Matter and Dark Energy, the expanding universe, the early universe, and the formation and evolution of structure.',
      track=models.Course.TRACK_UNDERGRAD,
      pdf_allowed=False,
      audit_allowed=False,
      ),
    'cos333': models.Course(
      department='COS',
      number=333,
      title='Advanced Programming Techniques',
      description='This is a course about the practice of programming.  Programming is more than just writing code.  Programmers must also assess tradeoffs, choose among design alternatives, debug and test, improve performance, and maintain software written by themselves &amp; others. At the same time, they must be concerned with compatibility, robustness, and reliability, while meeting specifications.  Students will have the opportunity to develop these skills by working on their own code and in group projects.',
      track=models.Course.TRACK_UNDERGRAD,
      pdf_allowed=False,
      audit_allowed=False,
      ),
    'cos432': models.Course(
      department='COS',
      number=432,
      title='Information Security',
      description='Course goals: learn how to design a secure system, probe systems for weaknesses, write code with fewer security bugs, use crypto libraries correctly, protect (or breach!) privacy, and use your powers ethically. Main topics: basic cryptography, system security, network security, firewalls, malware, web security, privacy technologies, cryptocurrencies, human factors, physical security, economics, and ethics of security.',
      track=models.Course.TRACK_UNDERGRAD,
      pdf_allowed=False,
      audit_allowed=False,
      ),
    'cos518': models.Course(
      department='COS',
      number=518,
      title='Advanced Computer Systems',
      description='COS-518 is a graduate course in computer systems. Its goals are: (1) To understand the core concepts of computer systems, rather than particular implementation details.  (2) To understand the state of the art in distributed, storage, mobile, and operating systems.  (3) To understand how to engage in cutting-edge systems research and development.  This course assumes a basic familiarity with computer systems and networking concepts.',
      track=models.Course.TRACK_GRAD,
      pdf_allowed=False,
      audit_allowed=False,
      ),
    'isc233': models.Course(
      department='ISC',
      number=233,
      title='An Integrated, Quantitative Introduction to the Natural Sciences II',
      description='An integrated, mathematically and computationally sophisticated introduction to physics and chemistry, drawing on examples from biological systems.  This year long, four course sequence is a multidisciplinary course taught across multiple departments with the following faculty: C. Callan, J. Shaevitz (PHY); H. Yang (CHM); O. Troyanskaya (COS); P. Andolfatto (EEB); E. Wieschaus, M. Wuhr (MOL); B. Bratton, J. Gadd, A. Mayer, Q. Wang (LSI).  Five hours of lecture, one three-hour lab, one three-hour precept, one required evening problem session.',
      track=models.Course.TRACK_UNDERGRAD,
      pdf_allowed=False,
      audit_allowed=False,
      )
    },
  'crosslistings': {
    'ast401': [models.CrossListing(department='PHY',number=401)],
    'cos432': [models.CrossListing(department='ELE', number=432)],
    'isc233': [
      models.CrossListing(department='CHM', number=233),
      models.CrossListing(department='COS', number=233),
      models.CrossListing(department='MOL', number=233),
      models.CrossListing(department='PHY', number=233)
      ],
    },
  'offerings': {
    'ast401': models.Offering(
      registrar_guid=1184000726,
      start_date=datetime.date(2018, 2, 5),
      end_date=datetime.date(2018, 5, 15),
      ),
    'cos333': models.Offering(
      registrar_guid=1184002065,
      start_date=datetime.date(2018, 2, 5),
      end_date=datetime.date(2018, 5, 15),
      ),
    'cos432': models.Offering(
      registrar_guid=1184002074,
      start_date=datetime.date(2018, 2, 5),
      end_date=datetime.date(2018, 5, 15),
      ),
    'cos518': models.Offering(
      registrar_guid=1184002098,
      start_date=datetime.date(2018, 2, 5),
      end_date=datetime.date(2018, 5, 15),
      ),
    'isc233': models.Offering(
      registrar_guid=1184009380,
      start_date=datetime.date(2018, 2, 5),
      end_date=datetime.date(2018, 5, 15),
      ),
    },
  'offering-instructors': {
    'ast401': ['alpha'],
    'cos333': ['bravo', 'charlie'],
    'cos432': ['delta'],
    'cos518': ['echo'],
    'isc233': ['foxtrot', 'alpha', 'delta']
    },
  'instructors': {
    'alpha': models.Instructor(
      employee_id='000000001', first_name='prof', last_name='Alpha'),
    'bravo': models.Instructor(
      employee_id='000000002', first_name='Prof', last_name='Bravo'),
    'charlie': models.Instructor(
      employee_id='000000003', first_name='PRof', last_name='Charlie'),
    'delta': models.Instructor(
      employee_id='000000004', first_name='PROf', last_name='Delta'),
    'echo': models.Instructor(
      employee_id='000000005', first_name='PROF', last_name='Echo'),
    'foxtrot': models.Instructor(
      employee_id='000000006',
      first_name='pROF',
      last_name='Foxtrot',
      full_name='pROF Foxtrot!'),
    },
    'sections': {
      'ast401': {
        'L01': models.Section(
          number=40300,
          section_id='L01',
          status=models.Section.STATUS_OPEN,
          capacity=999,
          enrollment=30),
        },
      'cos333': {
        'L01': models.Section(
          number=40160,
          section_id='L01',
          status=models.Section.STATUS_OPEN,
          capacity=160,
          enrollment=128),
        },
      'cos432': {
        'L01': models.Section(
          number=40184,
          section_id='L01',
          status=models.Section.STATUS_OPEN,
          capacity=40,
          enrollment=30),
        },
      'cos518': {
        'S01': models.Section(
          number=42951,
          section_id='S01',
          status=models.Section.STATUS_OPEN,
          capacity=30,
          enrollment=22),
        },
      'isc233': {
        'L01': models.Section(
          number=42038,
          section_id='L01',
          status=models.Section.STATUS_OPEN,
          capacity=20,
          enrollment=18),
        'C01': models.Section(
          number=42040,
          section_id='C01',
          status=models.Section.STATUS_OPEN,
          capacity=40,
          enrollment=18),
        'B01': models.Section(
          number=42041,
          section_id='B01',
          status=models.Section.STATUS_OPEN,
          capacity=20,
          enrollment=18),
        },
      },
    'meetings': {
      'ast401': {
        'L01': [
          models.Meeting(
            building='Peyton Hall',
            room='145',
            number=1,
            start_time=datetime.time(13, 30),
            end_time=datetime.time(14, 50),
            day=models.Meeting.DAY_MONDAY),
          models.Meeting(
            building='Peyton Hall',
            room='145',
            number=1,
            start_time=datetime.time(13, 30),
            end_time=datetime.time(14, 50),
            day=models.Meeting.DAY_WEDNESDAY),
          ]
        },
      'cos333': {
        'L01': [
          models.Meeting(
            building='Thomas Laboratory',
            room='003',
            number=1,
            start_time=datetime.time(11, 00),
            end_time=datetime.time(12, 20),
            day=models.Meeting.DAY_TUESDAY),
          models.Meeting(
            building='Thomas Laboratory',
            room='003',
            number=1,
            start_time=datetime.time(11, 00),
            end_time=datetime.time(12, 20),
            day=models.Meeting.DAY_THURSDAY)
          ]
        },
      'cos432': {
        'L01': [
          models.Meeting(
            building='Friend Center',
            room='004',
            number=1,
            start_time=datetime.time(11, 00),
            end_time=datetime.time(12, 20),
            day=models.Meeting.DAY_TUESDAY),
          models.Meeting(
            building='Friend Center',
            room='004',
            number=1,
            start_time=datetime.time(11, 00),
            end_time=datetime.time(12, 20),
            day=models.Meeting.DAY_THURSDAY)
          ]
        },
      'cos518': {
        'S01': [
          models.Meeting(
            building='Sherrerd Hall',
            room='001',
            number=1,
            start_time=datetime.time(9, 00),
            end_time=datetime.time(10, 20),
            day=models.Meeting.DAY_MONDAY),
          models.Meeting(
            building='Sherrerd Hall',
            room='001',
            number=1,
            start_time=datetime.time(9, 00),
            end_time=datetime.time(10, 20),
            day=models.Meeting.DAY_WEDNESDAY)
          ]
        },
      'isc233': {
        'L01': [
          models.Meeting(
            building='Carl C. Icahn Laboratory',
            room='101',
            number=1,
            start_time=datetime.time(10, 0),
            end_time=datetime.time(10, 50),
            day=models.Meeting.DAY_MONDAY),
          models.Meeting(
            building='Carl C. Icahn Laboratory',
            room='101',
            number=1,
            start_time=datetime.time(10, 0),
            end_time=datetime.time(10, 50),
            day=models.Meeting.DAY_WEDNESDAY),
          models.Meeting(
            building='Carl C. Icahn Laboratory',
            room='101',
            number=1,
            start_time=datetime.time(10, 0),
            end_time=datetime.time(10, 50),
            day=models.Meeting.DAY_FRIDAY),
          ],
        'C01': [
          models.Meeting(
            building='Carl C. Icahn Laboratory',
            room='100',
            number=1,
            start_time=datetime.time(19, 30),
            end_time=datetime.time(20, 50),
            day=models.Meeting.DAY_WEDNESDAY),
          ],
        'B01': [
          models.Meeting(
            building='Thomas Laboratory',
            room='012',
            number=1,
            start_time=datetime.time(13, 30),
            end_time=datetime.time(16, 20),
            day=models.Meeting.DAY_TUESDAY),
          ],
        },
      },
  }
