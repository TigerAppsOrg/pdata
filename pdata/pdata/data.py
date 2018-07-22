# pdata/pdata/data.py
# pdata
# Author: Rushy Panchal
# Date: January 12th, 2017
# Description: Interface for data providers.

import typing

_registry = {}

class _BaseDataProvider(type):
  '''
  Interface for data providers. A data provider consists of all tasks to
  update and acquire data, as well as any other tasks that are required. A
  task consists of a combination of a function and a schedule with which to
  execute it.

  If a Django app subclasses the DataProvider the class, it will be registered
  as a provider and its tasks will bea dded to a global pdata scheduler.

  To define this, `DataProvider` should be subclassed:

  .. code:: python

    class ExampleDataProvider(DataProvider):
      @property
      def tasks(self) -> List[dict]:
        return [...]
  '''
  def __new__(meta, name, bases, class_dict):
    cls = type.__new__(meta, name, bases, class_dict)
    original_module = cls.__module__.replace('.data', '')
    _registry[original_module] = cls()
    return cls
  
class DataProvider(metaclass=_BaseDataProvider):
  @property
  def tasks(self) -> typing.List[dict]:
    '''
    Return the list of tasks to execute with the task scheduler. This property
    must be overridden in child classes to dictate the actual tasks required
    for that data provider. Essentially, the task is defined as a dictionary of
    tasks and options that are executed with Celery Beat.

    For example, in a data provider which is defined by the Django app 'example'
    where the only task that needs to be executed on a schedule is an 'update'
    function (that needs to be executed every hour), the task definitions
    would be

    .. code:: python

      [
        {'task': 'example.update',
         'schedule': crontab(minute=0)}
      ]

    In this case, `example.update` would be a function available with that
    import.

    :return: task definitions for the data provider

    :see: http://docs.celeryproject.org/en/v4.1.0/userguide/periodic-tasks.html#entries
    '''
    raise NotImplementedError("DataProvider.tasks must be overridden.")

def get_provider(name) -> DataProvider:
  return _registry[name]
