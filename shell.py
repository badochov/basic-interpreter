# noinspection PyUnresolvedReferences
import readline
import sys

from basic import Basic
from errors.error import Error
from file_interpreter import print_error


def main(debug: bool = False) -> None:
    while True:
        text = input("basic > ")
        try:
            results = Basic.run(text, "<stdin>", True, debug)
            for result in results:
                print(result)
        except Error as err:
            print_error(err)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(True)
    else:
        main()
