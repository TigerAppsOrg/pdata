# pdata/pdata/settings.py
# pdata
# Author: Michael Friedman
# Date: December 1st, 2017
# Description: Django settings.

import os
import sys
import logging

from pdata import utils

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ENV = os.getenv('ENV', 'development')
SECRET_KEY = os.getenv(
  'SECRET_KEY', '-@8$+sra*9xl%+ed@h)%3mzs(@vsar_0zg6jq*q!&y^vx3ar3!')
DEBUG = (ENV == 'development')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')

TESTING = (ENV == 'test' or
  (len(sys.argv) >= 2 and sys.argv[1] == 'test'))

### Application Definition
INSTALLED_APPS = [
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',

  # Datasets
  'courses',
]

# No datasets so far...
PDATA_DATASETS = []
INSTALLED_APPS.extend(PDATA_DATASETS)

MIDDLEWARE = [
  'django.middleware.security.SecurityMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pdata.urls'
WSGI_APPLICATION = 'pdata.wsgi.application'

### Database
import dj_database_url
DATABASES = {
  'default': dj_database_url.config(default='sqlite:///db.sqlite3'),
}

### Password Validation
AUTH_PASSWORD_VALIDATORS = [
  {
    'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
  },
  {
    'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
  },
  {
    'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
  },
  {
    'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
  },
]

### Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_TZ = True

### Celery
import djcelery
djcelery.setup_loader()
CELERY_BROKER_URL = os.getenv('REDIS_URL', '')
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
CELERYBEAT_SCHEDULE = utils.load_celery_tasks(PDATA_DATASETS)

### Test settings
if TESTING:
  LOGGING = {}
  logging.disable(logging.CRITICAL + 1)

  # Allow test datasets to be imported.
  sys.path.append(os.path.join(BASE_DIR, 'pdata', 'tests'))
