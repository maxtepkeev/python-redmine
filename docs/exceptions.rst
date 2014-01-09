Exceptions
==========

Python Redmine tries it's best to provide human readable errors in all situations. This
is the list of all exceptions that Python Redmine can throw:

``BaseRedmineError``
    Base exception class for Redmine exceptions

``ResourceError``
    Unsupported Redmine resource exception

``AuthError``
    Invalid authentication details

``ImpersonateError``
    Invalid impersonate login provided

``ResourceSetIndexError``
    Index doesn't exist in the ResourceSet

``ResourceSetFilterParamError``
    Resource set filter method expects to receive either a list or tuple

``ResourceBadMethodError``
    Resource doesn't support the requested method, e.g. get()

``ResourceFilterError``
    Resource doesn't support requested filter(s)

``ResourceNoFiltersProvidedError``
    No filter(s) provided

``ResourceAttrError``
    Resource doesn't have the requested attribute

``ResourceVersionMismatchError``
    Resource isn't supported on specified Redmine version
