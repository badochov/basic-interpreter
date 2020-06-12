# noinspection PyUnresolvedReferences
import readline
import sys
from typing import Any

from basic import Basic
from errors.error import Error


def print_error(message: Any) -> None:
    print("\033[31;1m", file=sys.stderr, end="")
    print(message, file=sys.stderr)
    print("\033[0m", file=sys.stderr, end="")


def main(debug: bool = False) -> None:
    basic = Basic()
    while True:
        text = input("fun-lang > ")
        try:
            results = basic.run(text, "<stdin>", True, debug)
            for result in results:
                print(result)
        except Error as err:
            print_error(err)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(True)
    else:
        main()
