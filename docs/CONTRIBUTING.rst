Contribution Guide
==================

Repository Guidelines
---------------------

Git's entire goal is to keep a working record of all changes to the code.
Developers should strive to keep this record clean and easy to understand.

1. Commit messages should be descriptive and contain both a title and body
   unless the content of the commit is very minimal. Avoid using
   :code:`$ git commit -m`. Instead, use :code:`$ git commit` to write a
   succinct and detailed message. For example,

   .. code:: text

      Fix export CLI --csv bug

      The bug was caused because in Python 3.x, filter() and map() return
      iterators (i.e. filter/map objects) instead of the evaluated list.

2. Follow the `Git Branching Workflow <https://git-scm.com/book/en/v2/Git-Branching-Branching-Workflows>`_.
   The :code:`master` branch is reserved for production-ready code; any code
   ready to be tested should be merged into :code:`dev` branch. :code:`dev` is
   pushed to the staging server and :code:`master` is pushed to the production
   server, as necessary. Any features, bug fixes, or other work should be done
   separately in an appropriately named branch. These branches are generally
   prefixed with :code:`dev` (such as :code:`dev-api-refactor`). Bug fixes, on
   the other hand, would be prefixed with :code:`bugfix` (such as
   :code:`bugfix-17`, referring to an issue 17).

3. Try to commit small changes frequently. For example, do not have
   "batch" commits where you introduce multiple new features or bug fixes at
   once. Each commit should be focused on a specific feature, bug fix, or
   concept. You should *never* use :code:`$ git commit -a`; review all files
   being added to ensure that each commit is coherent. This can be done using
   :code:`git status` and :code:`git add {set of files}`.

4. Do not force push (:code:`$ git push -f` or :code:`$ git push --force`) to
   any upstream branch.

5. Do not add derived/generated files (i.e. compilation results, be those from
   JSX, SCSS, or any other language) to the repository. In general, only commit
   source code; anything that results from a build tool should not be committed.
   Generated files can be regenerated as needed. However, certain auto-generated
   files (such as Django's migrations) *should* be committed if they are
   considered source. On a similar note, static assets (such as minified JS
   libraries or images) are not to be included in a repository.

6. Do not add confidential or secure data to the repository, including API keys.
   Git maintains an entire history of the repository, and so removing such data
   requires rewriting the repository history, which is tedious and invalidates
   all other clones. Instead, data such as API keys should be consumed by the
   project in the form of environment variables.

Status Checks
^^^^^^^^^^^^^

Status checks must pass before merging into a protected branch
(i.e. :code:`master`). To do so, you can only push :code:`master` *after*
pushing your current branch (and waiting for status checks to pass).
In addition, you should never commit to :code:`master` directly, as GitHub
will reject those commits. More importantly, all merges to :code:`master`
should come through pull requests.

As a review of the repository guidelines, this is the expected workflow:

1. Checkout new branch for development
2. Edit files
3. Review changes
4. Decide on files to commit
5. Commit with proper title and description
6. Push current branch first and wait for status checks to pass
7. Merge with :code:`dev` and then push
8. Submit a pull request

.. code:: bash

  $ git checkout -b dev-docs     # (1)
  $ emacs pdata/settings.py      # (2)
  $ git diff                     # (3)
  $ git add pdata/settings.py    # (4)
  $ git commit                   # (5)
  $ git push origin dev-docs     # (6)
  $ git checkout dev             # (7)
  $ git merge dev-docs
  $ git push

:note: 
  It is vital that you do **not** commit to :code:`master` directly.
  If you do, a push to :code:`master` will be rejected and you will need to
  reset your master branch to the prior commit.

Style Guidelines
----------------

In general, follow the style of the file you are working on. This should be
(and remain) consistent across all files of the project. Most importantly, keep
readability and maintability in mind at all times.

In particular, every function and class should document its parameters
and expected types, return value and type, and any errors or warnings raised.
Example usage for non-intuitive functions are also useful.

Furthermore, each file should contain a header with the file path (from the
project root directory), project, author(s), creation date, and description:

.. code:: python

  # pdata/settings.py
  # pdata
  # Author: Rushy Panchal
  # Date: November 15th, 2017
  # Description: Django configuration.

For Python code, follow `PEP8 <https://www.python.org/dev/peps/pep-0008/>`_
as much as possible.

Some key takeaways:

- Use two (2) spaces for indentation, not tabs.
- File headers are mandatory.
- Lines should not exceed 80 characters.
- When splitting up a line onto multiple lines, each additional level should be
  indented twice (except for documentation).
- Arguments are split up if they span more than a line. If all of the arguments
  fit on the next line, put them on the next line. If they do not all fit on the
  next line, put each argument on a separate line.
- If your code needs significant explanation, consider refactoring.

Organization Guidelines
-----------------------

Maintaining a separation of responsibilities by splitting up the project into
separate components is important. It ensures that components can be maintained,
improved, deployed, and scaled independently, which simplifies development.

To that end, follow the `12-Factor App <https://12factor.net/>`_ guidelines.
Putting in extra initial effort to organize and design the project well ensures
that our future devlepment is smoother and hassle-free.
