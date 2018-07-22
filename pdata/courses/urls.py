# pdata/courses/urls.py
# pdata
# Author: Rushy Panchal
# Date: July 21st, 2018

from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register('listings', views.CourseViewset)
router.register('crosslistings', views.CrossListingViewset)
router.register('semesters', views.SemesterViewset)
router.register('instructors', views.InstructorViewset)
router.register('offerings', views.OfferingViewset)
router.register('sections', views.SectionViewset)
router.register('meetings', views.MeetingViewset)

urlpatterns = router.urls
