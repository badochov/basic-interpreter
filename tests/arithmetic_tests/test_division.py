from basic import Basic
from errors.invalid_syntax_error import InvalidSyntaxError
from errors.rt_error import RTError
from lang_types.lang_number import LangNumber
from tests.utilities import run_test


def test_wrong_syntax_division() -> None:
    basic = Basic()

    run_test(
        basic, " let _ = 42/", "test_wrong_order_division", None, InvalidSyntaxError
    )
    run_test(
        basic, " let _ = 42.5/", "test_wrong_order_div_float", None, InvalidSyntaxError,
    )
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


def test_integer_division() -> None:
    basic = Basic()

    run_test(
        basic, " let _ = 4 / +2", "test_positive_int_division", LangNumber, None, 4 / 2,
    )
    run_test(
        basic, " let _ = -4 / -2", "test_negative_int_div", LangNumber, None, -4 / -2,
    )
    run_test(basic, " let _ = 4 / -2", "test_mixed_int_div", LangNumber, None, 4 / -2)


def test_float_division() -> None:
    basic = Basic()

    run_test(
        basic,
        " let _ = 4.5 / +2.3",
        "test_pos_float_div",
        LangNumber,
        None,
        4.5 / +2.3,
    )
    run_test(
        basic,
        " let _ = -4.5 / -2.3",
        "test_neg_float_div",
        LangNumber,
        None,
        -4.5 / -2.3,
    )
    run_test(
        basic,
        " let _ = 4.5 / -2.3",
        "test_mixed_float_div",
        LangNumber,
        None,
        4.5 / -2.3,
    )
