# noinspection PyUnresolvedReferences
import readline

from basic import Basic

while True:
    text = input("basic > ")
    result, error = Basic.run(text, "<stdin>")

    if error:
        print(error)
    else:
        print(result)
