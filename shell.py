# noinspection PyUnresolvedReferences
import readline
import sys

from basic import Basic


def main(debug: bool = False) -> None:
    while True:
        text = input("basic > ")
        result, error = Basic.run(text, "<stdin>", True, debug)

        if error:
            print(error)
        else:
            print(result)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(True)
    else:
        main()
