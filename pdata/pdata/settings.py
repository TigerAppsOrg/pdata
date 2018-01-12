# pdata/pdata/settings.py
# pdata
# Author: Michael Friedman
# Date: December 1st, 2017
# Description: Django settings.

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ENV = os.getenv('ENV', 'development')
SECRET_KEY = os.getenv(
  'SECRET_KEY', '-@8$+sra*9xl%+ed@h)%3mzs(@vsar_0zg6jq*q!&y^vx3ar3!')
DEBUG = (ENV == 'development')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')

# Application definition

INSTALLED_APPS = [
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',

  # pdata
  'core',
]

MIDDLEWARE = [
  'django.middleware.security.SecurityMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pdata.urls'
WSGI_APPLICATION = 'pdata.wsgi.application'

# Database

import dj_database_url
DATABASES = {
  'default': dj_database_url.config(default='sqlite:///db.sqlite3'),
}

# Password validation

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

# Internationalization

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_TZ = True
