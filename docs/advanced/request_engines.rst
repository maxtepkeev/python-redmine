Request Engines
===============

.. versionadded:: 2.0.0

Python-Redmine has an extensible and customizable request engine system that allows to define
how requests to Redmine are made. Basically a request engine is a Python class that inherits
from :class:`redminelib.engines.BaseEngine` class and redefines a few methods to achieve the
needed behaviour. Engine can be set while configuring a ``redmine`` object, after it's set,
there is nothing else to be done to use it, i.e. it will be used by Python-Redmine automatically
while making requests to Redmine.

Engines
-------

Sync
++++

Default engine in Standard Edition. Requests are made in a sequential fashion, i.e. one by one. There
is nothing to do to use it, but just for the purpose of example, this is how we can explicitly ask
Python-Redmine to use it:

.. code-block:: python

   from redminelib import engines, Redmine

   redmine = Redmine('https://redmine.url', engine=engines.SyncEngine)

Thread
++++++

*Available only in Pro Edition*.

Default engine in Pro Edition. Requests are made in an asynchronous fashion using Python threads. The
amount of threads is calculated by Python-Redmine automatically, but can be adjusted manually passing
``workers`` argument to the ``Redmine`` class:

.. code-block:: python

   from redminelib import engines, Redmine

   redmine = Redmine('https://redmine.url', engine=engines.ThreadEngine, workers=4)

Process
+++++++

*Available only in Pro Edition*.

Requests are made in an asynchronous fashion using Python processes. The amount of processes is
calculated by Python-Redmine automatically, but can be adjusted manually passing ``workers`` argument
to the ``Redmine`` class:

.. code-block:: python

   from redminelib import engines, Redmine

   redmine = Redmine('https://redmine.url', engine=engines.ProcessEngine, workers=4)

.. note::

   Please keep in mind that currently only read operations are possible using async engines, all other
   types of operations, i.e. create/update/delete are made using sync engine.

Session
-------

Sometimes there is a need to change engine/connection options only for one or few requests.
Python-Redmine provides a convenient ``session()`` context manager for that. Options that can
be redefined are all keyword arguments accepted by ``Redmine`` class:

.. code-block:: python

   with redmine.session(workers=24):
       issues = redmine.issue.all()
       projects = redmine.project.all()

   with redmine.session(username='jsmith', password='secret'):
       issue = redmine.issue.create(project_id=123, subject='foo')

Custom Engine
-------------

It is possible to create additional engines if needed. To do that, create a class and inherit it from
``engines.BaseEngine`` class. The only methods that must be implemented are ``create_session()`` and
``process_bulk_request()``, please see code of ``engines.BaseEngine`` for details. Below you will find
methods and attributes which can be redefined in your custom engine:

.. autoclass:: redminelib.engines.BaseEngine
   :members: create_session, construct_request_kwargs, request, bulk_request, process_bulk_request, process_response
