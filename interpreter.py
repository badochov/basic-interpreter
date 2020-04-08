# noinspection PyUnresolvedReferences
import readline
import sys

from basic import Basic

if len(sys.argv) < 2:
    print("Usage python interpreter.py <file_name>")
    exit(1)

file_name = sys.argv[1]
with open(file_name, "r") as f:
    code = f.read()

result, error = Basic.run(code, file_name)

if error:
    print(error)
else:
    print(result)
