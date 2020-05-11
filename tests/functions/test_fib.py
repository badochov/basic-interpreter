from basic import Basic
from lang_types.lang_function import LangFunction
from lang_types.lang_number import LangNumber
from tests.utilities import run_test


def fib(n: int, a: int = 0, b: int = 1) -> int:
    if n == 0:
        return a
    return fib(n - 1, b, a + b)


def test_fib_naive() -> None:
    basic = Basic()
    run_test(
        basic,
        "let fib n = if n <2 then n else fib (n-1) + fib (n-2)",
        "test_fib_naive_part1",
        LangFunction,
        None,
    )
    for i in range(5):
        run_test(
            basic,
            f"let _ = fib {i}",
            f"test_naive_part{i + 1}",
            LangNumber,
            None,
            fib(i),
        )


def test_fib_opt() -> None:
    basic = Basic()
    run_test(
        basic,
        "let fib_pom a b n = if n == 0 then a else fib_pom (b) (a+b) (n-1)",
        "test_fib_opt_part0",
        LangFunction,
        None,
    )
    run_test(
        basic, "let fib = fib_pom 0 1", "test_fib_opt_part0.5", LangFunction, None,
    )
    for i in range(5):
        run_test(
            basic,
            f"let _ = fib {i}",
            f"test_fib_opt_part{i + 1}",
            LangNumber,
            None,
            fib(i),
        )
