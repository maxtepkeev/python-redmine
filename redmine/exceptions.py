class BaseRedmineError(Exception):
    """Base exception class for Redmine exceptions"""
    def __init__(self, *args, **kwargs):
        super(BaseRedmineError, self).__init__(*args, **kwargs)


class ResourceError(BaseRedmineError):
    """Unsupported Redmine resource exception"""
    def __init__(self):
        super(ResourceError, self).__init__('Unsupported redmine resource')


class NoFileError(BaseRedmineError):
    """File doesn't exist exception"""
    def __init__(self):
        super(NoFileError, self).__init__("Can't upload the file that doesn't exist")


class ResourceNotFoundError(BaseRedmineError):
    """Resource not found"""
    def __init__(self):
        super(ResourceNotFoundError, self).__init__("Requested resource doesn't exist")


class AuthError(BaseRedmineError):
    """Invalid authentication details"""
    def __init__(self):
        super(AuthError, self).__init__('Invalid authentication details')


class ImpersonateError(BaseRedmineError):
    """Invalid impersonate login provided"""
    def __init__(self):
        super(ImpersonateError, self).__init__("Impersonate login provided doesn't exist or isn't active")


class ServerError(BaseRedmineError):
    """Redmine internal error"""
    def __init__(self):
        super(ServerError, self).__init__('Redmine returned internal error, perhaps you are doing something wrong')


class ValidationError(BaseRedmineError):
    """Redmine validation error"""
    def __init__(self, error):
        super(ValidationError, self).__init__(error)


class ResourceSetIndexError(BaseRedmineError):
    """Index doesn't exist in the ResourceSet"""
    def __init__(self):
        super(ResourceSetIndexError, self).__init__('Resource not available by requested index')


class ResourceSetFilterParamError(BaseRedmineError):
    """Resource set filter method expects to receive either a list or tuple"""
    def __init__(self):
        super(ResourceSetFilterParamError, self).__init__('Method expects to receive either a list or tuple of ids')


class ResourceBadMethodError(BaseRedmineError):
    """Resource doesn't support the requested method, e.g. get()"""
    def __init__(self):
        super(ResourceBadMethodError, self).__init__("Resource doesn't support the requested method")


class ResourceFilterError(BaseRedmineError):
    """Resource doesn't support requested filter(s)"""
    def __init__(self):
        super(ResourceFilterError, self).__init__("Resource doesn't support requested filter(s)")


class ResourceNoFiltersProvidedError(BaseRedmineError):
    """No filter(s) provided"""
    def __init__(self):
        super(ResourceNoFiltersProvidedError, self).__init__('Resource needs some filters to be filtered on')


class ResourceNoFieldsProvidedError(BaseRedmineError):
    """No field(s) provided"""
    def __init__(self):
        super(ResourceNoFieldsProvidedError, self).__init__('Resource needs some fields to be created/updated')


class ResourceAttrError(BaseRedmineError):
    """Resource doesn't have the requested attribute"""
    def __init__(self):
        super(ResourceAttrError, self).__init__("Resource doesn't have the requested attribute")


class NotSettableAttrError(BaseRedmineError):
    """Resource can't set attribute that doesn't exist or is read only"""
    def __init__(self):
        super(NotSettableAttrError, self).__init__("Can't set attribute that doesn't exist or is read only")


class VersionMismatchError(BaseRedmineError):
    """Feature isn't supported on specified Redmine version"""
    def __init__(self, feature):
        super(VersionMismatchError, self).__init__("{0} isn't supported on specified Redmine version".format(feature))


class ResourceVersionMismatchError(VersionMismatchError):
    """Resource isn't supported on specified Redmine version"""
    def __init__(self):
        super(ResourceVersionMismatchError, self).__init__('Resource')
