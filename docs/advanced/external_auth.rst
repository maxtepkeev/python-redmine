External Authentication
=======================

.. versionadded:: 0.5.1

It is possible to use Python Redmine as a provider for external authentication based on the
Redmine user database, e.g. imagine you are making a website and you want to only authenticate
your users if they provide the same login/password they use to login to Redmine:

.. code-block:: python

    username = 'john'    # username comes from the POST request on form submit
    password = 'qwerty'  # password comes from the POST request on form submit

    user = Redmine('https://redmine.url', username=username, password=password).auth()

If authentication succeeded, ``user`` variable will contain details about the current user, if
there was an error during authentication proccess, an ``AuthError`` exception will be thrown.

If you need more control, for example you want to return your own error message, you can
intercept ``AuthError`` exception and do what you need, for example:

.. code-block:: python

    from redmine.exceptions import AuthError

    username = 'john'    # username comes from the POST request on form submit
    password = 'qwerty'  # password comes from the POST request on form submit

    try:
        user = Redmine('https://redmine.url', username=username, password=password).auth()
    except AuthError:
        raise Exception('Invalid login or password provided')
