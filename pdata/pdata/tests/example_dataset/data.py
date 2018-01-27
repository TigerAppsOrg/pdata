# pdata/pdata/tests/example_dataset/data.py
# pdata
# Author: Rushy Panchal
# Date: January 27th, 2018
# Description: Example dataset definition.

import typing

from celery.schedules import crontab

from pdata.data import Dataset

class ExampleDataset(Dataset):
  @property
  def tasks(self) -> typing.List[dict]:
    return [
    {'task': 'example_dataset.tasks.refresh',
     'schedule': crontab(minute=0)},
    {'task': 'example_dataset.tasks.purge',
     'schedule': crontab(hour=0, minute=0)}
    ]
