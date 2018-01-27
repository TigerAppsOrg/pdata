# pdata/pdata/data.py
# pdata
# Author: Rushy Panchal
# Date: January 12th, 2017
# Description: Interface for datasets.

import abc
import typing

class Dataset(metaclass=abc.ABCMeta):
  '''
  Interface for datasets. A dataset consists of all tasks to update and
  acquire data, as well as any other tasks that are required. A task consists
  of a combination of a function and a schedule with which to execute it.

  If a Django app contains a value `data` which is an instance of
  `Dataset`, it is assumed to be a dataset with this form of task
  definitions, in which case the tasks will be added to a global pdata
  scheduler.

  To define this, a subclass of `Dataset` should be created for which an
  instance of the name `data` exists, as such:

  .. code:: python

    class ExampleDataset(Dataset):
      @property
      def tasks(self) -> List[dict]:
        return [...]

    data = ExampleDataset()

  .. note:: Dataset tasks

    A dataset *must* contain an instance of `Dataset`, named as `data`, if
    it has tasks that must be executed on a schedule. Otherwise, the tasks
    will not be found and consequently, not executed.

  '''
  @property
  @abc.abstractmethod
  def tasks(self) -> typing.List[dict]:
    '''
    Return the list of tasks to execute with the task scheduler. This property
    must be overridden in child classes to dictate the actual tasks required
    for that dataset. Essentially, the task is defined as a dictionary of
    tasks and options that are executed with Celery Beat.

    For example, in a dataset which is defined by the Django app 'dataset'
    where the only task that needs to be executed on a schedule is an
    'update' function (that needs to be executed every hour), the task
    definitions would be

    .. code:: python

      [
        {'task': 'dataset.update',
         'schedule': crontab(minute=0)}
      ]

    In this case, `dataset.update` would be a function available with that
    import.

    :return: task definitions for the dataset

    :see: http://docs.celeryproject.org/en/v4.1.0/userguide/periodic-tasks.html#entries
    '''
    raise NotImplementedError("Dataset.tasks must be overridden.")
