# pyresult
A Python Result type featuring 2.x compatible type annotations


A small example showing how you can use custom errors, implementing the Error interface, to chain failable operations
in a type safe manner.

For smaller, isolated examples of the Result API I suggest checking the documentation comments - they should all have
examples.
```python
from checked import *

def hit_rest_api(url):
    # type: (str) -> Result[str, Error]
    return Result(Ok("im fine"))


def parse_json(json):
    # type: (str) -> Result[Dict[str, str], Error]
    return Result(Ok({"foo": "bar"}))


def print_foo(json):
    # type: (Dict[str, str]) -> None
    print(json)


def main():
    # type: () -> None
    hit_rest_api("example.com")\
        .and_then(lambda r: parse_json(r))\
         .or_else(lambda _: {"foo": "baz"})\
        .if_ok(print_foo)


if __name__ == '__main__':
    main()

```
