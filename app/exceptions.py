class InvalidDataException(Exception):
    def __init__(self, message: str, field=""):
        super().__init__(message)
        self.field = field


class RateLimitException(Exception):
    pass


class NotFoundException(Exception):
    pass
