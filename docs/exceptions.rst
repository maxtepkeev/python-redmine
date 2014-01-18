Exceptions
==========

Python Redmine tries it's best to provide human readable errors in all situations. This
is the list of all exceptions that Python Redmine can throw:

``BaseRedmineError``
    Base exception class for Redmine exceptions

``ResourceError``
    Unsupported Redmine resource exception

``NoFileError``
    File doesn't exist exception

``ResourceNotFoundError``
    Requested resource doesn't exist

``AuthError``
    Invalid authentication details

``ImpersonateError``
    Invalid impersonate login provided

``ServerError``
    Redmine internal error

``ValidationError(error)``
    Redmine validation errors occured on create/update resource

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

``ResourceNoFieldsProvidedError``
    No field(s) provided

``ResourceAttrError``
    Resource doesn't have the requested attribute

``NotSettableAttrError``
    Resource can't set attribute that doesn't exist or is read only

``VersionMismatchError(feature)``
    Feature isn't supported on specified Redmine version

``ResourceVersionMismatchError``
    Resource isn't supported on specified Redmine version
