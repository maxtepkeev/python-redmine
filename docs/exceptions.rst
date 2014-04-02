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

``ConflictError``
    Resource version on the server is newer than client's

``AuthError``
    Invalid authentication details

``ImpersonateError``
    Invalid impersonate login provided

``ServerError``
    Redmine internal error

``RequestEntityTooLargeError``
    Size of the request exceeds the capacity limit on the server

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

``ReadonlyAttrError``
    Resource can't set attribute that is read only

``VersionMismatchError(feature)``
    Feature isn't supported on specified Redmine version

``ResourceVersionMismatchError``
    Resource isn't supported on specified Redmine version

``ResultSetTotalCountError``
    ResultSet hasn't been yet evaluated and cannot yield a total_count

``CustomFieldValueError``
    Custom fields should be passed as a list of dictionaries
