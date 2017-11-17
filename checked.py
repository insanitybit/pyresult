# from typing_extensions import Protocol
try:
    from typing import Union, TypeVar, Generic, Callable, Optional, Dict
    T = TypeVar('T')
    U = TypeVar('U')
    E = TypeVar('E')
    O = TypeVar('O')
except:
    pass


class Error(object):
    @staticmethod
    def try_from(e):
        # type: (Union[str, Exception]) -> Error
        _ = e
        raise TypeError("Error class is not to be used directly: try_from")

    def why(self):
        # type: () -> str
        raise TypeError("Error class is not to be used directly: why")


class Ok(Generic[T]):
    def __init__(self, t):
        # type: (T) -> None
        self.t = t

    def get(self):
        # type: () -> T
        return self.t


class Err(Generic[E]):
    def __init__(self, e):
        # type: (E) -> None
        self.inner = e

    def get(self):
        # type: () -> E
        return self.inner


class Result(Generic[T, E]):
    def __init__(self, t):
        # type: (Union[Ok[T], Err[E]]) -> None
        self.inner = t

    def is_ok(self):
        # type: () -> bool
        if isinstance(self.inner, Ok):
            return True
        elif isinstance(self.inner, Err):
            return False
        else:
            raise TypeError("Result variant type invalid: " + str(type(self.inner)))

    def is_err(self):
        # type: () -> bool
        if isinstance(self.inner, Ok):
            return False
        elif isinstance(self.inner, Err):
            return True
        else:
            raise TypeError("Result variant type invalid: " + str(type(self.inner)))

    def ok(self):
        # type: () -> Optional[T]
        if isinstance(self.inner, Ok):
            return self.inner.get()
        elif isinstance(self.inner, Err):
            return None
        else:
            raise TypeError("Result variant type invalid: " + str(type(self.inner)))

    def err(self):
        # type: () -> Optional[E]
        if isinstance(self.inner, Ok):
            return None
        elif isinstance(self.inner, Err):
            return self.inner.get()
        else:
            raise TypeError("Result variant type invalid: " + str(type(self.inner)))

    def unwrap(self, msg=""):
        # type: (str) -> T
        _ = msg
        if isinstance(self.inner, Ok):
            return self.inner.get()
        elif isinstance(self.inner, Err):
            raise TypeError("Unwrap on an err value: " + msg or str(self.inner))
        else:
            raise TypeError("Result variant type invalid: " + str(type(self.inner)))

    def unwrap_err(self, msg=""):
        # type: (str) -> E
        if isinstance(self.inner, Ok):
            raise TypeError("unwrap_err called on Ok: " + msg)
        elif isinstance(self.inner, Err):
            return self.inner.get()
        else:
            raise TypeError("Result variant type invalid: " + str(type(self.inner)))

    def unwrap_or(self, t):
        # type: (T) -> T
        if isinstance(self.inner, Ok):
            return self.inner.get()
        elif isinstance(self.inner, Err):
            return t
        else:
            raise TypeError("Result variant type invalid: " + str(type(self.inner)))

    def unwrap_or_else(self, f):
        # type: (Callable[[E], T]) -> T
        if isinstance(self.inner, Ok):
            return self.inner.get()
        elif isinstance(self.inner, Err):
            return f(self.inner.get())
        else:
            raise TypeError("Result variant type invalid: " + str(type(self.inner)))

    def map(self, f):
        # type: (Callable[[T], U]) -> Result[U, E]
        if isinstance(self.inner, Ok):
            return Result(Ok(f(self.inner.get())))
        elif isinstance(self.inner, Err):
            return Result(Err(self.inner.get()))
        else:
            raise TypeError("Result variant type invalid: " + str(type(self.inner)))

    def map_err(self, f):
        # type: (Callable[[E], O]) -> Result[T, O]
        if isinstance(self.inner, Ok):
            return Result(Ok(self.inner.get()))
        elif isinstance(self.inner, Err):
            return Result(Err(f(self.inner.get())))
        else:
            raise TypeError("Result variant type invalid: " + str(type(self.inner)))

    def if_ok(self, f):
        # type:(Callable[[T], U]) -> None
        if isinstance(self.inner, Ok):
            f(self.inner.get())

    def if_err(self, f):
        # type:(Callable[[E], None]) -> None
        if isinstance(self.inner, Err):
            f(self.inner.get())

    def and_then(self, f):
        # type:(Callable[[T], Result[U, E]]) -> Result[U, E]
        if isinstance(self.inner, Ok):
            return f(self.inner.get())
        elif isinstance(self.inner, Err):
            return Result(Err(self.inner.get()))
        else:
            raise TypeError("Result variant type invalid: " + str(type(self.inner)))

    def or_else(self, f):
        # type:(Callable[[E], Result[T, O]]) -> Result[T, O]
        if isinstance(self.inner, Ok):
            return Result(Ok(self.inner.get()))
        elif isinstance(self.inner, Err):
            return f(self.inner.get())
        else:
            raise TypeError("Result variant type invalid: " + str(type(self.inner)))
