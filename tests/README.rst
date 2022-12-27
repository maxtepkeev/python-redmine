Running tests
=============

To run tests you will need these packages:

* pytest
* pytest-cov
* requests

For your convenience they are all listed in the ``requirements.txt`` file in this directory.
After all dependencies are installed you can run tests with this command:

.. code-block:: bash

    $ pytest --cov-config=.coveragerc --cov=redminelib
