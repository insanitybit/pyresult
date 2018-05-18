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
