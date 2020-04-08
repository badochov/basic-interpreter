# noinspection PyUnresolvedReferences
import readline

from basic import Basic

# text = """
#         let fib =
#             let fib_pom a b n =
#                 if n == 0 then
#                     a
#                 else
#                     fib_pom b (a+b) (n-1)
#             in
#                 fib_pom 0 1
#         """
# Basic.run(text, "fdasfdas")

while True:
    text = input("basic > ")
    result, error = Basic.run(text, "<stdin>")

    if error:
        print(error)
    else:
        print(result)
