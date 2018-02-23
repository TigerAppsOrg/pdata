# pdata/courses/models.py
# pdata
# Author: Rushy Panchal
# Date: February 22nd, 2018
# Description: Courses dataset models.

from django.db import models

class Course(models.Model):
  '''
  The `Course` model represents all of the data contained within a course.
  This is data that does *not* change between semesters.
  '''
  title = models.CharField(max_length=255)
  description = models.TextField()
  registrar_id = models.PositiveIntegerField()
  distribution_area = models.CharField(max_length=3, db_index=True, null=True)

  department = models.CharField(max_length=3, db_index=True)
  number = models.PositiveSmallIntegerField(db_index=True)
  letter = models.CharField(max_length=1, default="")

  pdf_allowed = models.BooleanField(default=True)
  audit_allowed = models.BooleanField(default=True)

  class Meta:
    unique_together = ('department', 'number')

class Semester(models.Model):
  '''
  The `Semester` model represents a single semester, which occurs at a single
  point in time.
  '''
  TERM_FALL = 1
  TERM_SPRING = 2
  term = models.PositiveSmallIntegerField(choices=(
    (TERM_FALL, 'Fall'),
    (TERM_SPRING, 'Spring')
    ), db_index=True)

  year = models.PositiveSmallIntegerField(db_index=True)

class Instructor(models.Model):
  '''
  The `Instructor` model represents a single instructor. An instructor may
  teach multiple courses across multiple semesters.
  '''
  first_name = models.CharField(max_length=255)
  last_name = models.CharField(max_length=255)
  full_name = models.CharField(max_length=255, null=True)
  employee_id = models.CharField(max_length=9, db_index=True)

class CourseOffering(models.Model):
  '''
  The `CourseOffering` model represents all of the offerings of a single
  course. For example, there are unique offering of some courses per semester,
  and others which are only taught in a single semester.
  '''
  registrar_guid = models.PositiveIntegerField(db_index=True)
  course = models.ForeignKey(Course, on_delete=models.CASCADE)
  semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
  instructor = models.ManyToManyField(Instructor)

  start_date = models.DateTimeField()
  end_date = models.DateTimeField()

class CrossListing(models.Model):
  '''
  The `CrossListing` model represents each of the different
  (department, number) pairs that a course is listed under. For example,
  COS 342 is cross-listed as MAT 375.
  '''
  course = models.ForeignKey(Course, on_delete=models.CASCADE)

  department = models.CharField(max_length=3, db_index=True)
  number = models.PositiveSmallIntegerField(db_index=True)
  letter = models.CharField(max_length=1, default="")
