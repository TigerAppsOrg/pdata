# pdata/pdata/utils.py
# pdata
# Author: Rushy Panchal
# Date: January 27th, 2018
# Description: Misc. utilities.

import typing

import sys

from django.utils.module_loading import import_string

import pdata.data

def load_celery_tasks(sources: typing.List[str]) -> dict:
  '''
  Load Celery tasks from the provided sources. Tasks are loaded from any
  `data.Dataset` class present as the value `data` in the source.

  :return: loaded tasks
  '''
  tasks = {}
  for s in sources:
    try:
      dataset_def = import_string('{source}.data'.format(source=s))
    except ImportError as e:
      raise e
    else:
      if isinstance(dataset_def, pdata.data.Dataset):
        task_def = dataset_def.tasks
        for t in task_def:
          task_name = '{source}:{name}'.format(
            source=s,
            # Turn dataset.func into dataset-func
            name=t['task'].replace('.', '-'))
          tasks[task_name] = t

  return tasks
