import sys

from basic import Basic


def main(file_name: str) -> None:
    with open(file_name, "r") as f:
        code = f.read()
    basic = Basic()

    results = basic.run(code, file_name)
    for result in results:
        print(result)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage python " + sys.argv[0] + " <file_name>")
        exit(1)
    main(sys.argv[1])
