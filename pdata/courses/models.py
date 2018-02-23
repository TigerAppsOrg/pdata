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
  registrar_id = models.PositiveIntegerField(unique=True)
  distribution_area = models.CharField(max_length=3, db_index=True, null=True)

  department = models.CharField(max_length=3, db_index=True)
  number = models.PositiveSmallIntegerField(db_index=True)
  #: A letter is sometimes appended to course numbers (i.e. ENV 200A, ENV200B,
  #: etc.).
  letter = models.CharField(max_length=1, default="")

  pdf_allowed = models.BooleanField(default=True, db_index=True)
  audit_allowed = models.BooleanField(default=True, db_index=True)

  class Meta:
    unique_together = ('department', 'number', 'letter')

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

  class Meta:
    unique_together = ('term', 'year')

class Instructor(models.Model):
  '''
  The `Instructor` model represents a single instructor. An instructor may
  teach multiple courses across multiple semesters.
  '''
  first_name = models.CharField(max_length=255)
  last_name = models.CharField(max_length=255)

  #: A full_name is presented in the Registrar data, which means that it may
  #: be possible that the `first_name last_name` does not equal to the
  #: full_name. If they are equal, however, the value will be null.
  full_name = models.CharField(max_length=255, null=True)
  employee_id = models.CharField(max_length=9, unique=True, db_index=True)

class CourseOffering(models.Model):
  '''
  The `CourseOffering` model represents all of the offerings of a single
  course. For example, there are unique offering of some courses per semester,
  and others which are only taught in a single semester.
  '''
  registrar_guid = models.PositiveIntegerField(unique=True, db_index=True)
  course = models.ForeignKey(Course, on_delete=models.CASCADE)
  semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
  instructor = models.ManyToManyField(Instructor)

  start_date = models.DateField()
  end_date = models.DateField()

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

  class Meta:
    unique_together = ('course', 'department', 'number', 'letter')
