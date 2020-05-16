from basic import Basic
from errors.invalid_syntax_error import InvalidSyntaxError
from tests.utilities import run_test


def test_wrong_syntax_multiplication() -> None:
    basic = Basic()
    run_test(
        basic,
        " let _ = *42",
        "test_wrong_order_multiplication",
        None,
        InvalidSyntaxError,
    )
    run_test(
        basic,
        " let _ = *42.5",
        "test_wrong_order_multiplication_float",
        None,
        InvalidSyntaxError,
    )
