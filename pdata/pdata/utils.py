# pdata/pdata/utils.py
# pdata
# Author: Rushy Panchal
# Date: January 27th, 2018
# Description: Misc. utilities.

import typing

import sys

from django.utils.module_loading import import_string
from django.db import models

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

def bulk_upsert_item(
  t: typing.Type[models.Model],
  defaults: typing.Optional[dict] = None,
  **kwargs) -> typing.Tuple[models.Model, bool]:
  '''
  Allow for bulk upserts when an object is created. In particular, it acts just
  like `obj.update_or_create(defaults=defaults, **kwargs)` but instead of
  saving the object on creation, it is simply instantiated. The object can then
  be saved to the database using `bulk_create(obj...)`.

  :param t: type of model
  :param defaults: default values to insert
  :param kwargs: filter kwargs

  :return: tuple of object and boolean flag if created or not
  '''
  # See: https://docs.djangoproject.com/en/2.0/ref/models/querysets/#get-or-create
  params = {k: v for k, v in kwargs.items() if '__' not in k}
  params.update({k: v() if callable(v) else v for k, v in defaults.items()})

  created = False
  try:
    obj = t.objects.get(**kwargs)
  except t.DoesNotExist:
    obj = t(**params)
    # Newly-created object is *not* saved so it can be bulk-created later on.
    created = True
  else:
    # Update all the fields to the new values
    dirty = False
    for k, v in params.items():
      if getattr(obj, k) != v:
        setattr(obj, k, v)
        dirty = True
    if dirty:
      obj.save()

  return (obj, created)

