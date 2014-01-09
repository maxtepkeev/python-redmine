class BaseRedmineError(Exception):
    """Base exception class for Redmine exceptions"""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class ResourceError(BaseRedmineError):
    """Unsupported Redmine resource exception"""
    def __init__(self):
        super(ResourceError, self).__init__('Unsupported redmine resource')


class AuthError(BaseRedmineError):
    """Invalid authentication details"""
    def __init__(self):
        super(AuthError, self).__init__('Invalid authentication details')


class ImpersonateError(BaseRedmineError):
    """Invalid impersonate login provided"""
    def __init__(self):
        super(ImpersonateError, self).__init__("Impersonate login provided doesn't exist or isn't active")


class ResourceSetIndexError(BaseRedmineError):
    """Index doesn't exist in the ResourceSet"""
    def __init__(self):
        super(ResourceSetIndexError, self).__init__('Resource not available by requested index')


class ResourceSetFilterParamError(BaseRedmineError):
    """Resource set filter method expects to receive either a list or tuple"""
    def __init__(self):
        super(ResourceSetFilterParamError, self).__init__("Method expects to receive either a list or tuple of ids")


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
        super(ResourceNoFiltersProvidedError, self).__init__("Resource needs some filters to be filtered on")


class ResourceAttrError(BaseRedmineError):
    """Resource doesn't have the requested attribute"""
    def __init__(self):
        super(ResourceAttrError, self).__init__("Resource doesn't have the requested attribute")


class ResourceVersionMismatchError(BaseRedmineError):
    """Resource isn't supported on specified Redmine version"""
    def __init__(self):
        super(ResourceVersionMismatchError, self).__init__("Resource isn't supported on specified Redmine version")
