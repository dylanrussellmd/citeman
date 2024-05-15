class CriticalFieldException(Exception):
    def __init__(self, field):
        self.field = field
        super().__init__("Missing critical field: ")

class KeyExistsError(ValueError):
    def __init__(self, key) -> None:
        self.key = key
        super().__init__("Key already exists: ")

class FieldExistsError(ValueError):
    def __init__(self, field) -> None:
        self.field = field
        super().__init__("Field already exists: ")

class FieldMissingError(ValueError):
    def __init__(self, field) -> None:
        self.field = field
        super().__init__("Field missing: ")

class LibraryEmptyError(ValueError):
    def __init__(self) -> None:
        super().__init__("Library is empty.")

class HistoryEmptyError(ValueError):
    def __init__(self) -> None:
        super().__init__("Query history is empty.")