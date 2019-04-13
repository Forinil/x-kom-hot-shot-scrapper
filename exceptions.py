class ProcessingException(Exception):
    pass


class PageLoadingException(ProcessingException):
    pass


class JSProcessingException(ProcessingException):
    pass
