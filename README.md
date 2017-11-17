# pyresult
A Python Result type featuring 2.x compatible type annotations

from checked import *
```python
class RestError(Error):
    def __init__(self, e):
        # type: (Union[str, Exception]) -> None
        self.inner = e

    @staticmethod
    def try_from(e):
        # type: (Union[str, Exception]) -> RestError
        return RestError(e)

    def why(self):
        # type: () -> str
        if isinstance(self.inner, str):
            return "Rest Client Error: " + self.inner
        elif isinstance(self.inner, Exception):
            return "Rest Client Error: " + str(self.inner)
        else:
            raise TypeError("Expected String or Exception, got: " + str(type(self.inner)))

class JsonParseError(Error):
    def __init__(self, e):
        # type: (Union[str, Exception]) -> None
        self.inner = e

    @staticmethod
    def try_from(e):
        # type: (Union[str, Exception]) -> JsonParseError
        return JsonParseError(e)

    def why(self):
        # type: () -> str
        if isinstance(self.inner, str):
            return "Json Parse Error: " + self.inner
        elif isinstance(self.inner, Exception):
            return "Json Parse Error: " + str(self.inner)


def hit_rest_api(url):
    # type: (str) -> Result[str, Error]
    return Result(Ok("im fine"))


def parse_json(json):
    # type: (str) -> Result[Dict[str, str], Error]
    return Result(Ok({"foo": "bar"}))


def print_foo(json):
    # type: (Dict[str, str]) -> None
    print(json)


if __name__ == '__main__':
    hit_rest_api("example.com")\
        .and_then(lambda r: parse_json(r))\
        .if_ok(print_foo)
```
