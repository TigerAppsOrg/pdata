Project Setup
=============

Quick Start
-----------

This project uses Python 3.6. Before proceeding, make sure to
`install it <https://www.python.org/downloads/>`_ and have it set as your
default Python version (recommended that you use a Python version manager like
`pyenv <https://github.com/pyenv/pyenv>`_).

To set up your development environment, you can run the automated setup script
:code:`configure.sh` in the root of the repository:

.. code:: bash

  $ ./configure.sh

This will install all Python dependencies you need for the project. You can also rerun this script upon pulling changes to install new dependencies
if more become required.


Dependencies
------------

Below we list the Python dependencies required for the project (note that
these are automatically installed by the :code:`configure.sh` script).

- Django (1.11)
- Django REST Framework
