class NSXSDKException(Exception):
    pass


class ResourceNotFound(NSXSDKException):

    def __init__(self, resource):
        message = "Resource %s not found." % resource
        super(ResourceNotFound, self).__init__(message)


class IncorrectRequest(NSXSDKException):
    pass
