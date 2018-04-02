# pdata/courses/models.py
# pdata
# Author: Rushy Panchal
# Date: February 22nd, 2018
# Description: Courses dataset models.

from django.db import models
from django.core.validators import MaxValueValidator

class Course(models.Model):
  '''
  The `Course` model represents all of the data contained within a course.
  This is data that does *not* change between semesters.
  '''
  title = models.CharField(max_length=255)
  description = models.TextField()

  distribution_area = models.CharField(max_length=3, db_index=True, null=True)
  department = models.CharField(max_length=3, db_index=True)
  number = models.PositiveSmallIntegerField(db_index=True)
  #: A letter is sometimes appended to course numbers (i.e. ENV 200A, ENV200B,
  #: etc.).
  letter = models.CharField(max_length=1, default="")

  TRACK_UNDERGRAD = 1
  TRACK_GRAD = 2
  track = models.PositiveSmallIntegerField(choices=(
    (TRACK_UNDERGRAD, 'Undergraduate'),
    (TRACK_GRAD, 'Graduate')
    ))

  pdf_allowed = models.BooleanField(default=True, db_index=True)
  audit_allowed = models.BooleanField(default=True, db_index=True)

  class Meta:
    unique_together = ('department', 'number', 'letter')

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

  start_date = models.DateField()
  end_date = models.DateField()

  #: Registrar-assigned term ID.
  term_id = models.PositiveIntegerField(unique=True)

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

  #: Provided by the Registrar with instructor listings.
  employee_id = models.CharField(max_length=9, unique=True, db_index=True)

class Offering(models.Model):
  '''
  The `Offering` model represents all of the offerings of a single
  course. For example, there are unique offering of some courses per semester,
  and others which are only taught in a single semester.
  '''
  #: The GUID is always unique, because it is the concatenation of the
  #: semester's term_id and a per-semester, unique course_id.
  registrar_guid = models.PositiveIntegerField(unique=True, db_index=True)

  course = models.ForeignKey(Course, on_delete=models.CASCADE)
  semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

  #: An instructor can teach many different offerings, and a single offering
  #: can be taught by multiple instructors.
  instructor = models.ManyToManyField(Instructor)

  start_date = models.DateField()
  end_date = models.DateField()

  class Meta:
    unique_together = ('course', 'semester')

class Section(models.Model):
  '''
  The `Section` model represents a single class for a course. For example,
  an offered course will have multiple classes, as lectures or precepts.
  '''
  offering = models.ForeignKey(Offering, on_delete=models.CASCADE)

  #: Per-offering unique number assigned to each meeting.
  number = models.PositiveIntegerField()

  #: Per-offering unique number assigned to each meeting.
  section_id = models.CharField(max_length=3)

  #: Status of the section.
  STATUS_OPEN = 1
  STATUS_CLOSED = 2
  STATUS_CANCELLED = 3
  status = models.PositiveSmallIntegerField(choices=(
    (STATUS_OPEN, 'Open'),
    (STATUS_CLOSED, 'Closed'),
    (STATUS_CANCELLED, 'Cancelled'),
    ))

  capacity = models.PositiveIntegerField()

  #: The enrollment should always be, at most, the capacity.
  enrollment = models.PositiveIntegerField()

  class Meta:
    unique_together = ('offering', 'section_id')

class Meeting(models.Model):
  '''
  The `Meeting` model is for a single, well, meeting of a section.

  Generally, there is a one-to-one mapping between sections and meetings.
  However, it is possible for a single class (such as a lecture) to have
  multiple meeting times.
  '''
  section = models.ForeignKey(Section, on_delete=models.CASCADE)

  building = models.CharField(max_length=100)
  room = models.CharField(max_length=10)

  #: Per-section unique number.
  number = models.PositiveSmallIntegerField()

  start_time = models.TimeField()
  end_time = models.TimeField()

  #: Days of the week where 0 is Sunday, 1 is Monday, and so forth.
  DAY_SUNDAY = 0
  DAY_MONDAY = 1
  DAY_TUESDAY = 2
  DAY_WEDNESDAY = 3
  DAY_THURSDAY = 4
  DAY_FRIDAY = 5
  DAY_SATURDAY = 6
  day = models.PositiveSmallIntegerField(choices=(
    (DAY_SUNDAY, 'Sunday'),
    (DAY_MONDAY, 'Monday'),
    (DAY_TUESDAY, 'Tuesday'),
    (DAY_WEDNESDAY, 'Wednesday'),
    (DAY_THURSDAY, 'Thursday'),
    (DAY_FRIDAY, 'Friday'),
    (DAY_SATURDAY, 'Saturday'),
    ))

  class Meta:
    unique_together = ('section', 'number', 'day')
