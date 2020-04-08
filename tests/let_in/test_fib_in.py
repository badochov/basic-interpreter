from basic import Basic
from lang_types.lang_number import LangNumber
from errors.invalid_syntax_error import InvalidSyntaxError
from tests.utilities import run_test
from lang_types.lang_function import LangFunction
from lang_types.lang_number import LangNumber


def fib(n: int, a: int = 0, b: int = 1) -> int:
    if n == 0:
        return a
    return fib(n - 1, b, a + b)


def test_fib_naive() -> None:
    basic = Basic()
    run_test(
        basic,
        """
        let fib =
            let fib_pom a b n =
                if n == 0 then
                    a
                else
                    fib_pom b (a+b) (n-1)
            in
                fib_pom 0 1
        """,
        "test_fib_naive_part1",
        LangFunction,
        None,
    )
    for i in range(42):
        run_test(
            basic,
            f"let _ = fib {i}",
            f"test_fib_in_part{i+1}",
            LangNumber,
            None,
            fib(i),
        )
