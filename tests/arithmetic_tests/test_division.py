from basic import Basic
from errors.invalid_syntax_error import InvalidSyntaxError
from errors.rt_error import RTError
from tests.utilities import run_test


def test_wrong_syntax_division() -> None:
    basic = Basic()

    run_test(
        basic, " let _ = /42", "test_wrong_order_division", None, InvalidSyntaxError
    )
    run_test(
        basic, " let _ = /42.5", "test_wrong_order_div_float", None, InvalidSyntaxError,
    )


def test_division_by_zero() -> None:
    basic = Basic()

    run_test(basic, " let _ = 42/0", "test_integer division by zero", None, RTError)
    run_test(basic, " let _ = 42.5/0", "test_float division by zero", None, RTError)
