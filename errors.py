class BaseError(Exception):
    def __init__(self, *args):
        self.message = args[0] if args else None

    def __str__(self):
        if self.message:
            return f'{self.__class__.__name__}: {self.message}'
        return self.__class__.__name__


class FileFormatError(BaseError):
    pass
