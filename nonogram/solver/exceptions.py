class NonogramException(Exception):
    pass


class UnsolvableState(NonogramException):
    pass


class UnsolvableLine(UnsolvableState):
    pass
