# pdata/courses/tests/test_data.py
# pdata
# Author: Rushy Panchal
# Date: March 28th, 2018
# Description: Test data fetching/updating utilities.

import typing

from django.test import TestCase, SimpleTestCase

from pdata.courses import models, data

class TestUpdateTermData(TestCase):
  pass

EXPECTED_OBJECTS = {
  'semester': models.Semester(
    term=models.Semester.TERM_SPRING,
    year=2018,
    start_date='2018-02-05',
    end_date='2018-06-05',
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
    'qcb233': models.Course(
      department='QCB',
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
    'qcb233:': [
      models.CrossListing(department='CHM', number=233),
      models.CrossListing(department='COS', number=233),
      models.CrossListing(department='MOL', number=233),
      models.CrossListing(department='PHY', number=233)
      ],
    },
  'offerings': {
    'ast401': models.Offering(
      registrar_guid='1184000726',
      start_date='2018-02-05',
      end_date='2018-05-15',
      ),
    'cos333': models.Offering(
      registrar_guid='1184002065',
      start_date='2018-02-05',
      end_date='2018-05-15',
      ),
    'cos432': models.Offering(
      registrar_guid='1184002074',
      start_date='2018-02-05',
      end_date='2018-05-15',
      ),
    'cos518': models.Offering(
      registrar_guid='1184002098',
      start_date='2018-02-05',
      end_date='2018-05-15',
      ),
    'qcb233': models.Offering(
      registrar_guid='1184009380',
      start_date='2018-02-05',
      end_date='2018-05-15',
      ),
    },
  'offering-instructors': {
    'ast401': ['alpha'],
    'cos333': ['bravo', 'charlie'],
    'cos432': ['delta'],
    'cos518': ['echo'],
    'qcb233': ['foxtrot', 'alpha', 'delta']
    }
  'instructors': {
    'alpha': models.Instructor(
      employee_id='000000001', first_name='prof', last_name='Alpha'),
    'bravo': models.Instructor(
      employee_id='000000002', first_name='Prof', last_name='Bravo'),
    'charlie': models.Instructor(
      employee_id='000000003', first_name='PRof', last_name='Charlie'),
    'echo': models.Instructor(
      employee_id='000000004', first_name='PROf', last_name='Delta'),
    'delta': models.Instructor(
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
      'qcb233': {
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
            start_time='1:30 PM',
            end_time='02:50 PM',
            day=models.Meeting.DAY_MONDAY),
          models.Meeting(
            building='Peyton Hall',
            room='145',
            number=1,
            start_time='1:30 PM',
            end_time='02:50 PM',
            day=models.Meeting.DAY_WEDNESDAY),
          ]
        },
      'cos333': {
        'L01': [
          models.Meeting(
            building='Thomas Laboratory',
            room='003',
            number=1,
            start_time='11:00 AM',
            end_time='12:20 PM',
            day=models.Meeting.DAY_TUESDAY),
          models.Meeting(
            building='Thomas Laboratory',
            room='003',
            number=1,
            start_time='11:00 AM',
            end_time='12:20 PM',
            day=models.Meeting.DAY_THURSDAY)
          ]
        },
      'cos432': {
        'L01': [
          models.Meeting(
            building='Friend Center',
            room='004',
            number=1,
            start_time='11:00 AM',
            end_time='12:20 PM',
            day=models.Meeting.DAY_TUESDAY),
          models.Meeting(
            building='Friend Center',
            room='004',
            number=1,
            start_time='11:00 AM',
            end_time='12:20 PM',
            day=models.Meeting.DAY_TUESDAY)
          ]
        },
      'cos518': {
        'S01': [
          models.Meeting(
            building='Sherrerd Hall',
            room='001',
            number=1,
            start_time='09:00 AM',
            end_time='10:20 AM',
            day=models.Meeting.DAY_MONDAY),
          models.Meeting(
            building='Sherrerd Hall',
            room='001',
            number=1,
            start_time='09:00 AM',
            end_time='10:20 AM',
            day=models.Meeting.DAY_WEDNESDAY)
          ]
        },
      'qcb233': {
        'L01': [
          models.Meeting(
            building='Carl C. Icahn Laboratory',
            room='101',
            number=1,
            start_time='10:00 AM',
            end_time='10:50 AM',
            day=models.Meeting.DAY_MONDAY),
          models.Meeting(
            building='Carl C. Icahn Laboratory',
            room='101',
            number=1,
            start_time='10:00 AM',
            end_time='10:50 AM',
            day=models.Meeting.DAY_WEDNESDAY),
          models.Meeting(
            building='Carl C. Icahn Laboratory',
            room='101',
            number=1,
            start_time='10:00 AM',
            end_time='10:50 AM',
            day=models.Meeting.DAY_FRIDAY),
          ],
        'C01': [
          models.Meeting(
            building='Carl C. Icahn Laboratory',
            room='100',
            number=1,
            start_time='07:30 PM',
            end_time='08:50 PM',
            day=models.Meeting.DAY_WEDNESDAY),
          ],
        'B01': [
          models.Meeting(
            building='Thomas Laboratory',
            room='012',
            number=1,
            start_time='01:30 PM',
            end_time='04:20 PM',
            day=models.Meeting.DAY_TUESDAY),
          ],
        },
      },
  }
