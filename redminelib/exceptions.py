"""
Python-Redmine tries it's best to provide human readable errors in all situations.
This is a list of all exceptions or warnings that Python-Redmine can throw/raise.
"""


class BaseRedmineWarning(Warning):
    """
    Base warning class for Redmine warnings.
    """


class PerformanceWarning(BaseRedmineWarning):
    """
    Warning raised when there's a possible performance impact.
    """


class BaseRedmineError(Exception):
    """
    Base exception class for Redmine exceptions.
    """


class ResourceError(BaseRedmineError):
    """
    Unsupported Redmine resource exception.
    """
    def __init__(self):
        super().__init__('Unsupported Redmine resource')


class NoFileError(BaseRedmineError):
    """
    File doesn't exist or is empty exception.
    """
    def __init__(self):
        super().__init__("Can't upload a file that doesn't exist or is empty")


class FileObjectError(BaseRedmineError):
    """
    File-like object isn't supported as it doesn't support the read(size) method.
    """
    def __init__(self):
        super().__init__("File-like object doesn't support the read(size) method")


class ResourceNotFoundError(BaseRedmineError):
    """
    Requested resource doesn't exist.
    """
    def __init__(self):
        super().__init__("Requested resource doesn't exist")


class ConflictError(BaseRedmineError):
    """
    Resource version on the server is newer than on the client.
    """
    def __init__(self):
        super().__init__('Resource version on the server is newer than on the client')


class AuthError(BaseRedmineError):
    """
    Invalid authentication details.
    """
    def __init__(self):
        super().__init__('Invalid authentication details')


class ImpersonateError(BaseRedmineError):
    """
    Invalid impersonate login provided.
    """
    def __init__(self):
        super().__init__("Impersonate login provided doesn't exist or isn't active")


class ServerError(BaseRedmineError):
    """
    Redmine internal error.
    """
    def __init__(self):
        super().__init__('Redmine returned internal error, check Redmine logs for details')


class RequestEntityTooLargeError(BaseRedmineError):
    """
    Size of the request exceeds the capacity limit on the server.
    """
    def __init__(self):
        super().__init__(
            "The requested resource doesn't allow POST requests or the size of the request exceeds the capacity limit")


class UnknownError(BaseRedmineError):
    """
    Redmine returned unknown error.
    """
    def __init__(self, status_code):
        self.status_code = status_code
        super().__init__(f'Redmine returned unknown error with the status code {status_code}')


class ValidationError(BaseRedmineError):
    """
    Redmine validation errors occurred on create/update resource.
    """
    def __init__(self, error):
        super().__init__(error)


class ResourceSetIndexError(BaseRedmineError):
    """
    Index doesn't exist in the ResourceSet.
    """
    def __init__(self):
        super().__init__('Resource not available by requested index')


class ResourceSetFilterLookupError(BaseRedmineError):
    """
    Resource set filter method received an invalid lookup in one of the filters.
    """
    def __init__(self, lookup, f):
        super().__init__(f'Received an invalid lookup "{lookup}" in "{f}" filter')


class ResourceBadMethodError(BaseRedmineError):
    """
    Resource doesn't support the requested method.
    """
    def __init__(self):
        super().__init__("Resource doesn't support the requested method")


class ResourceFilterError(BaseRedmineError):
    """
    Resource doesn't support requested filter(s).
    """
    def __init__(self):
        super().__init__("Resource doesn't support requested filter(s)")


class ResourceNoFiltersProvidedError(BaseRedmineError):
    """
    No filter(s) provided.
    """
    def __init__(self):
        super().__init__('Resource needs some filters to be filtered on')


class ResourceNoFieldsProvidedError(BaseRedmineError):
    """
    No field(s) provided.
    """
    def __init__(self):
        super().__init__('Resource needs some fields to be set to be created/updated')


class ResourceAttrError(BaseRedmineError, AttributeError):
    """
    Resource doesn't have the requested attribute.
    """
    def __init__(self):
        super().__init__("Resource doesn't have the requested attribute")


class ReadonlyAttrError(BaseRedmineError):
    """
    Resource can't set attribute that is read only.
    """
    def __init__(self):
        super().__init__("Can't set read only attribute")


class VersionFormatError(BaseRedmineError):
    """
    Version format provided isn't supported. SemVer is the only format accepted.
    """
    def __init__(self, version):
        super().__init__(
            f"Version in the {version} format isn't supported, please provide numeric version in the form of X.X.X")


class VersionMismatchError(BaseRedmineError):
    """
    Feature isn't supported on specified Redmine version.
    """
    def __init__(self, feature):
        super().__init__(f"{feature} isn't supported on specified Redmine version")


class ResourceVersionMismatchError(VersionMismatchError):
    """
    Resource isn't supported on specified Redmine version.
    """
    def __init__(self):
        super().__init__('Resource')


class ResultSetTotalCountError(BaseRedmineError):
    """
    ResultSet hasn't been yet evaluated and cannot yield a total_count.
    """
    def __init__(self):
        super().__init__('Total count is unknown before evaluation')


class CustomFieldValueError(BaseRedmineError):
    """
    Custom fields should be passed as a list of dictionaries.
    """
    def __init__(self):
        super().__init__(
            "Custom fields should be passed as a list of dictionaries in the form of [{'id': 1, 'value': 'foo'}]")


class ResourceRequirementsError(BaseRedmineError):
    """
    Resource requires specified Redmine plugin(s) to function.
    """
    def __init__(self, requirements):
        super().__init__('The following requirements must be installed for resource to function: {}'.format(
                ', '.join(' >= '.join(req) if isinstance(req, (list, tuple)) else req for req in requirements)))


class FileUrlError(BaseRedmineError):
    """
    URL provided to download a file can't be parsed.
    """
    def __init__(self):
        super().__init__("URL provided to download a file can't be parsed")


class ForbiddenError(BaseRedmineError):
    """
    Requested resource is forbidden.
    """
    def __init__(self):
        super().__init__('Requested resource is forbidden')


class JSONDecodeError(BaseRedmineError):
    """
    Unable to decode received JSON.
    """
    def __init__(self, response):
        self.response = response
        super().__init__(
            'Unable to decode received JSON, you can inspect exception\'s '
            '"response" attribute to find out what the response was')


class ExportNotSupported(BaseRedmineError):
    """
    Export functionality not supported by resource.
    """
    def __init__(self):
        super().__init__('Export functionality not supported by resource')


class ExportFormatNotSupportedError(BaseRedmineError):
    """
    The given format isn't supported by resource.
    """
    def __init__(self):
        super().__init__("The given format isn't supported by resource")


class HTTPProtocolError(BaseRedmineError):
    """
    Wrong HTTP protocol usage.
    """
    def __init__(self):
        super().__init__('Redmine url should start with HTTPS and not with HTTP')


class EngineClassError(BaseRedmineError):
    """
    Engine isn't a class or isn't a BaseEngine subclass.
    """
    def __init__(self):
        super().__init__("Engine isn't a class or isn't a BaseEngine subclass")
