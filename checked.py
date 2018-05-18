from typing import Union, TypeVar, Generic, Callable, Optional, Dict

T = TypeVar('T')
U = TypeVar('U')
E = TypeVar('E')
O = TypeVar('O')


class Error(object):
    def __init__(self, e):
        # type: (Union[str, Exception]) -> None
        if isinstance(e, str):
            self.e = e
        else:
            self.e = str(e)

    def why(self):
        # type: () -> str
        return self.e


class Ok(Generic[T]):
    """
    Represents the successful result of computation
    """
    def __init__(self, t):
        # type: (T) -> None
        self.t = t

    def get(self):
        # type: () -> T
        return self.t


class Err(Generic[E]):
    """
    Represents the unsuccessful result of computation
    """
    def __init__(self, e):
        # type: (E) -> None
        self.inner = e

    def get(self):
        # type: () -> E
        return self.inner


class Result(Generic[T, E]):
    """
    Result is a type that represents either success (Ok) or failure (Err).

    It is *heavily* inspired (effectively a direct translation) by Rust's
    Result type
    """
    def __init__(self, t):
        # type: (Union[Ok[T], Err[E]]) -> None
        self.inner = t

    def is_ok(self):
        # type: () -> bool
        """
        assert Result(Ok("Success!")).is_ok()

        :return: True if Ok, False if Err
        """
        if isinstance(self.inner, Ok):
            return True
        elif isinstance(self.inner, Err):
            return False
        else:
            raise TypeError("Result variant type invalid: " + str(type(self.inner)))

    def is_err(self):
        # type: () -> bool
        """
        assert Result(Ok("Success!")).is_ok()

        :return: True if Err, False if Ok
        """
        if isinstance(self.inner, Ok):
            return False
        elif isinstance(self.inner, Err):
            return True
        else:
            raise TypeError("Result variant type invalid: " + str(type(self.inner)))

    def ok(self):
        # type: () -> Optional[T]
        """
        Converts a Result[T, E] to an Optional[T]
        """
        if isinstance(self.inner, Ok):
            return self.inner.get()
        elif isinstance(self.inner, Err):
            return None
        else:
            raise TypeError("Result variant type invalid: " + str(type(self.inner)))

    def err(self):
        # type: () -> Optional[E]
        """
        Converts a Result[T, E] into an Optional[E]
        :return:
        """
        if isinstance(self.inner, Ok):
            return None
        elif isinstance(self.inner, Err):
            return self.inner.get()
        else:
            raise TypeError("Result variant type invalid: " + str(type(self.inner)))

    def unwrap(self, msg=""):
        # type: (str) -> T
        """
        Unwraps a result, yielding the content of an Ok.
        Throws exception on an Err
        """
        if isinstance(self.inner, Ok):
            return self.inner.get()
        elif isinstance(self.inner, Err):
            raise TypeError("Unwrap on an err value: " + msg or str(self.inner))
        else:
            raise TypeError("Result variant type invalid: " + str(type(self.inner)))

    def unwrap_err(self, msg=""):
        # type: (str) -> E
        """
        Unwraps a result, yielding the content of an Err.
        Throws exception on an Ok

        x = Result(Ok(2)) # type: Result[Ok(int), Err(str)]
        assert x.unwrap() == 2

        x= Result(Err("emergency failure")) # Result[Ok(int), Err(str)]
        x.unwrap() # Throws exception with `emergency failure`
        """
        if isinstance(self.inner, Ok):
            raise TypeError("unwrap_err called on Ok: " + msg)
        elif isinstance(self.inner, Err):
            return self.inner.get()
        else:
            raise TypeError("Result variant type invalid: " + str(type(self.inner)))

    def unwrap_or(self, t):
        # type: (T) -> T
        """
        Unwraps a result, yielding the content of an Ok. Else, it returns t.

        optb = 2
        x = Result(Ok(9))  # type: Result[Ok(int), Err(str)]
        assert x.unwrap_or(optb) == 9

        x = Result(Err("error"))  # type: Result[Ok(int), Err(str)]
        assert x.unwrap_or(optb) == optb
        """
        if isinstance(self.inner, Ok):
            return self.inner.get()
        elif isinstance(self.inner, Err):
            return t
        else:
            raise TypeError("Result variant type invalid: " + str(type(self.inner)))

    def unwrap_or_else(self, f):
        # type: (Callable[[E], T]) -> T
        """
        Returns the successful result of a computation or, on error, returns the
        value returned by `f`
        :param f: A function that takes an Error and returns a T
        :return:
        """
        if isinstance(self.inner, Ok):
            return self.inner.get()
        elif isinstance(self.inner, Err):
            return f(self.inner.get())
        else:
            raise TypeError("Result variant type invalid: " + str(type(self.inner)))

    def map(self, f):
        # type: (Callable[[T], U]) -> Result[U, E]
        """
        Maps a Result[T, E] to Result[U, E] by applying a function to
        a contained Ok value, leaving an Err value untouched.

        This function can be used to compose the results of two functions.

        line = "1\n2\n3\n4\n"
        for num in line.splitlines():
            res = parse_num(num)\
                .map(lambda i: i * 2)\
                .if_ok(lambda num: print(num))
        """

        if isinstance(self.inner, Ok):
            return Result(Ok(f(self.inner.get())))
        elif isinstance(self.inner, Err):
            return Result(Err(self.inner.get()))
        else:
            raise TypeError("Result variant type invalid: " + str(type(self.inner)))

    def map_err(self, f):
        # type: (Callable[[E], O]) -> Result[T, O]
        """
        Maps a Result[T, E] to Result[T, O] by applying a function to
        a contained Err value, leaving an Ok value untouched.

        This function can be used to compose the results of two functions.

        def stringify(x):
            return "error code: %s" % x

        x = Result(Ok(2)) # type: Result[Ok(int), Err(int)]
        assert x.map_err(stringify) == Result(Ok(2))

        x = Result(Err(13)) # type: Result[Ok(int), Err(int)]
        assert x.map_err(stringify) == Result(Err("error code: 13"))
        """
        if isinstance(self.inner, Ok):
            return Result(Ok(self.inner.get()))
        elif isinstance(self.inner, Err):
            return Result(Err(f(self.inner.get())))
        else:
            raise TypeError("Result variant type invalid: " + str(type(self.inner)))

    def if_ok(self, f):
        # type:(Callable[[T], U]) -> Optional[U]
        """
        Maps a Result[T, E] to an Optional[U], discarding E
        """
        if isinstance(self.inner, Ok):
            return f(self.inner.get())
        else:
            return None

    def if_err(self, f):
        # type:(Callable[[E], O]) -> Optional[O]
        """
        Maps a Result[T, E] to an Optional[O], discarding T
        """
        if isinstance(self.inner, Err):
            return f(self.inner.get())
        else:
            return None

    def and_then(self, f):
        # type:(Callable[[T], Result[U, E]]) -> Result[U, E]
        """
        Calls `f` if the result is Ok, otherwise returns the Err value of self.
        This function can be used for control flow based on Result values.

        # Example
        ```python
        def sq(x: int) -> Result[Ok(int), Err(int)]:
            return Result(Ok(x * x))

        def err(x: int) -> Result[Ok(int), Err(int)]::
            return Result(Err(x))

        assert Result(Ok(2)).and_then(sq).and_then(sq) == Result(Ok(16))
        assert Result(Ok(2)).and_then(sq).and_then(err) == Result(Err(4))
        assert Result(Ok(2)).and_then(err).and_then(sq) == Result(Err(2))
        assert Result(Err(3)).and_then(sq).and_then(sq) == Result(Err(3))
        ```
        """
        if isinstance(self.inner, Ok):
            return f(self.inner.get())
        elif isinstance(self.inner, Err):
            return Result(Err(self.inner.get()))
        else:
            raise TypeError("Result variant type invalid: " + str(type(self.inner)))

    def or_else(self, f):
        # type:(Callable[[E], O]) -> Result[T, O]
        """
        Calls `f` if the result is Err, otherwise returns the Ok value of self.

        This function can be used for control flow based on result values.

        def sq(x: int) -> Result[Ok(int), Err(int)>:
            return Result(Ok(x * x))

        def err(x: int) -> Result[Ok(int), Err(int)>:
            return Result(Err(x))

        assert Result(Ok(2)).or_else(sq).or_else(sq) == Result(Ok(2))
        assert Result(Ok(2)).or_else(err).or_else(sq) == Result(Ok(2))
        assert Result(Err(3)).or_else(sq).or_else(err) == Result(Ok(9))
        assert Result(Err(3)).or_else(err).or_else(err) == Result(Err(3))

        """

        if isinstance(self.inner, Ok):
            return Result(Ok(self.inner.get()))
        elif isinstance(self.inner, Err):
            return Result(Err(f(self.inner.get())))
        else:
            raise TypeError("Result variant type invalid: " + str(type(self.inner)))
