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

results = Basic.run(code, file_name, False)
for result, error in results:
    if error:
        print(error, file=sys.stderr)
    else:
        print(result)
        pass
