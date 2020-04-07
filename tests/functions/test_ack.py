from basic import Basic
from lang_types.lang_number import LangNumber
from errors.invalid_syntax_error import InvalidSyntaxError
from tests.utilities import run_test
from lang_types.lang_function import LangFunction
from lang_types.lang_number import LangNumber


def ack(m: int, n: int) -> int:
    if m == 0:
        return n + 1
    if m > 0 and n == 0:
        return ack(m - 1, 1)
    if m > 0 and n > 0:
        return ack(m - 1, ack(m, n - 1))


def test_ack() -> None:
    basic = Basic()
    run_test(
        basic,
        "let ack m n = if m ==0 then n+1 elif n ==0 and m>0 then ack (m-1) 1 elif m>0 and n>0 then ack (m-1) (ack (m) (n-1)) else 0",
        "test_ack_part1",
        LangFunction,
        None,
    )
    run_test(basic, "ack 2 2", "test_ack_part1", LangNumber, None, ack(2, 2))
    run_test(basic, "ack 2 1", "test_ack_part1", LangNumber, None, ack(2, 1))
    run_test(basic, "ack 3 1", "test_ack_part1", LangNumber, None, ack(3, 1))
    # run_test(basic, "ack 3 2", "test_ack_part1", LangNumber, None, 29)
    run_test(basic, "ack 1 2", "test_ack_part1", LangNumber, None, ack(1, 2))
    run_test(basic, "ack 1 3", "test_ack_part1", LangNumber, None, ack(1, 3))
    run_test(basic, "ack 1 1", "test_ack_part1", LangNumber, None, ack(1, 1))
