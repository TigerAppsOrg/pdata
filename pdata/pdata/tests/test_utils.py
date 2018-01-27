# pdata/pdata/tests/test_utils.py
# pdata
# Author: Rushy Panchal
# Date: January 27th, 2018
# Description: Tests for utility functions.

import sys

from django.test import SimpleTestCase
from celery.schedules import crontab

from pdata import utils

class TestLoadCeleryTasks(SimpleTestCase):
  '''
  Test the `utils.load_celery_tasks` function.
  '''
  def test_load(self):
    tasks = utils.load_celery_tasks(['example_dataset'])
    self.assertEquals(tasks, {
      'example_dataset:example_dataset-tasks-refresh': {
        'task': 'example_dataset.tasks.refresh',
        'schedule': crontab(minute=0)},
      'example_dataset:example_dataset-tasks-purge': {
        'task': 'example_dataset.tasks.purge',
        'schedule': crontab(hour=0, minute=0)}
      })
