# pdata/pdata/utils.py
# pdata
# Author: Rushy Panchal
# Date: January 27th, 2018
# Description: Misc. utilities.

import typing

import sys

from django.utils.module_loading import import_string
from django.db import models
from django.db import transaction

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

def bulk_upsert(
  q: typing.Type[models.query.QuerySet],
  hash_data: typing.Callable[[typing.Dict[str, typing.Any]], int],
  expected: typing.Iterable[typing.Dict[str, typing.Any]],
  delete: bool = False,
  ) -> typing.Dict[str, typing.Set[str]]:
  '''
  Bulk upsert objects. The queryset `q` is used to retrieve the existing
  objects, and `expected` is a list of dictionarys (mapping field names to
  values). One query is performed to find existing objects, and then the
  updates are performed individually while inserts/deletes are performed in
  bulk. The performance improvements come from the bulk insertions and single
  filter query.

  This operation is *not* performed atomically, so wrap the call to
  `bulk_upsert` in a `transaction.atomic` context if you require it to be
  atomic.

  For N existing objects (to update) and M objects to create, this performs
  N+2 database queries. In comparison, Django's `update_or_create` performs
  2(N+M) queries. More simply, `bulk_upsert` requires O(N+2) queries where N
  is the length of expected data set.

  :param q: queryset to retrieve existing objects
  :param hash_data: hash a dictionary representation of an object to a unique
    value (this will generally be some unique value in the object itself)
  :param expected: set of expected objects (represented as dictionaries) to
    upsert

  :return: set of unique values for each of: created, updated
  '''
  model_t = q.model

  obj_map = {} # Maps hashes to objects
  dict_map = {} # Maps hashes to dicts, each corresponding to an object.

  for obj, d in zip(q, q.values()):
    h = hash_data(d)
    obj_map[h] = obj
    dict_map[h] = d

  existing_hashes = frozenset(dict_map.keys())

  # Add in the expected values.
  expected_map = {hash_data(d): d for d in expected}
  expected_hashes = frozenset(expected_map.keys())
  dict_map.update(expected_map)

  # Operations to perform, and objects on which to perform them.
  to_update = expected_hashes & existing_hashes
  to_create = expected_hashes - existing_hashes

  # Update each object individually.
  for o in to_update:
    obj = obj_map[o]
    for k, v in dict_map[o].items():
      setattr(obj, k, v)
    obj.save()

  # Bulk insert newly-created objects.
  model_t.objects.bulk_create(
    map(lambda o: model_t(**dict_map[o]), to_create))

  return {
    'created': to_create,
    'updated': to_update,
    }
