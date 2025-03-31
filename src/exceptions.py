

class FileError(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class MissingArtist(KeyError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class ConnectionError(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidFile(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidID(KeyError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class MissingChart(KeyError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)