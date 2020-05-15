# noinspection PyUnresolvedReferences
import readline
import sys

from basic import Basic


def main(debug: bool = False) -> None:
    while True:
        text = input("basic > ")
        results = Basic.run(text, "<stdin>", True, debug)
        for result, error in results:
            if error:
                print(error, file=sys.stderr)
            else:
                print(result)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(True)
    else:
        main()
