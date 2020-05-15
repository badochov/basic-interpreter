import sys
from typing import Any

from basic import Basic


def print_error(message: Any) -> None:
    print("\033[31;1m", file=sys.stderr, end="")
    print(message, file=sys.stderr)
    print("\033[0m", file=sys.stderr, end="")


def main(file_name: str) -> None:
    with open(file_name, "r") as f:
        code = f.read()

    results = Basic.run(code, file_name, False)
    for result, error in results:
        if error:
            print_error(error)
        else:
            print(result)
            pass


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage python " + sys.argv[0] + " <file_name>")
        exit(1)
    main(sys.argv[1])
