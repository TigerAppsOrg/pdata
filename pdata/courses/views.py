# pdata/courses/views.py
# pdata
# Author: Rushy Panchal
# Date: July 21st, 2018

from rest_framework import viewsets

from . import models
from . import serializers

class CourseViewset(viewsets.ReadOnlyModelViewSet):
  queryset = models.Course.objects.all()
  serializer_class = serializers.CourseSerializer

class CrossListingViewset(viewsets.ReadOnlyModelViewSet):
  queryset = models.CrossListing.objects.all()
  serializer_class = serializers.CrossListingSerializer

class SemesterViewset(viewsets.ReadOnlyModelViewSet):
  queryset = models.Semester.objects.all()
  serializer_class = serializers.SemesterSerializer

class InstructorViewset(viewsets.ReadOnlyModelViewSet):
  queryset = models.Instructor.objects.all()
  serializer_class = serializers.InstructorSerializer

class OfferingViewset(viewsets.ReadOnlyModelViewSet):
  queryset = models.Offering.objects.all()
  serializer_class = serializers.OfferingSerializer

class SectionViewset(viewsets.ReadOnlyModelViewSet):
  queryset = models.Section.objects.all()
  serializer_class = serializers.SectionSerializer

class MeetingViewset(viewsets.ReadOnlyModelViewSet):
  queryset = models.Meeting.objects.all()
  serializer_class = serializers.MeetingSerializer
