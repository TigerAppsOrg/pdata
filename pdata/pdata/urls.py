# pdata/pdata/urls.py
# pdata
# Author: Michael Friedman
# Date: December 1st, 2017
# Description: Django root URL configuration.

from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
  url(r'^admin/', admin.site.urls),
]
