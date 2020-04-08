from basic import Basic
from lang_types.lang_number import LangNumber
from errors.invalid_syntax_error import InvalidSyntaxError
from tests.utilities import run_test
from lang_types.lang_function import LangFunction
from lang_types.lang_number import LangNumber


def inc(x: int) -> int:
    return x + 1


def add(x: int, y: int) -> int:
    return x + y


"""
let add x y = x + y
let inc = add 1
inc 2
add 21 37
inc 3
"""


def test_ack() -> None:
    basic = Basic()
    run_test(
        basic, "let add x y = x + y", "test_partial_part0", LangFunction, None,
    )
    run_test(
        basic, "let inc = add 1", "test_partial_part1", LangFunction, None,
    )

    for i in range(10):
        for j in range(10):
            run_test(
                basic,
                f"let _ = add {i} {j}",
                f"test_partials_part2.{i}.{j}",
                LangNumber,
                None,
                add(i, j),
            )
    for i in range(21):
        run_test(
            basic,
            f"let _ = inc {i}",
            f"test_partials_part3.{i}",
            LangNumber,
            None,
            inc(i),
        )
    for i in range(10):
        for j in range(10):
            run_test(
                basic,
                f"let _ = add {i} {j}",
                f"test_partials_part4.{i}.{j}",
                LangNumber,
                None,
                add(i, j),
            )
    for i in range(21):
        run_test(
            basic,
            f"let _ = inc {i}",
            f"test_partials_part5.{i}",
            LangNumber,
            None,
            inc(i),
        )
