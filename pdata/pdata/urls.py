# pdata/pdata/urls.py
# pdata
# Author: Michael Friedman
# Description: Django root URL configuration.
# Date: December 1st, 2017

from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
]
