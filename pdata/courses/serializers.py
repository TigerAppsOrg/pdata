# pdata/courses/serializers.py
# pdata
# Author: Rushy Panchal
# Date: July 21st, 2018

from rest_framework import serializers

from . import models

class CourseSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Course
    fields = '__all__'

class CrossListingSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.CrossListing
    fields = '__all__'

class SemesterSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Semester
    fields = '__all__'

class InstructorSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Instructor
    fields = '__all__'

class OfferingSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Offering
    fields = '__all__'

class SectionSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Section
    fields = '__all__'

class MeetingSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Meeting
    fields = '__all__'
