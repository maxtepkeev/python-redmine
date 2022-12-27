Running tests
=============

To run tests you will need these packages:

* coverage
* nose
* requests

For your convenience they are all listed in the ``requirements.txt`` file in this directory.
After all dependencies are installed you can run tests with this command:

.. code-block:: bash

    $ nosetests --with-coverage --cover-erase --cover-package=redminelib
