from basic import Basic
from lang_types.lang_number import LangNumber
from errors.invalid_syntax_error import InvalidSyntaxError
from tests.utilities import run_test


def test_wrong_syntax_multiplication() -> None:
    basic = Basic()

    run_test(
        basic,
        " let _ = 42*",
        "test_wrong_order_multiplication",
        None,
        InvalidSyntaxError,
    )
    run_test(
        basic,
        " let _ = 42.5*",
        "test_wrong_order_multiplication_float",
        None,
        InvalidSyntaxError,
    )
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


def test_integer_multiplication() -> None:
    basic = Basic()

    run_test(
        basic,
        " let _ = 4 * +2",
        "test_positive_integer_multiplication",
        LangNumber,
        None,
        4 * 2,
    )
    run_test(
        basic,
        " let _ = -4 * -2",
        "test_negative_integer_multiplication",
        LangNumber,
        None,
        -4 * -2,
    )
    run_test(
        basic,
        " let _ = 4 * -2",
        "test_mixed_integer_multiplication",
        LangNumber,
        None,
        4 * -2,
    )


def test_float_multiplication() -> None:
    basic = Basic()

    run_test(
        basic,
        " let _ = 4.5 * +2.3",
        "test_positive_float_multiplication",
        LangNumber,
        None,
        4.5 * 2.3,
    )
    run_test(
        basic,
        " let _ = -4.5 * -2.3",
        "test_negative_float_multiplication",
        LangNumber,
        None,
        -4.5 * -2.3,
    )
    run_test(
        basic,
        " let _ = 4.5 * -2.3",
        "test_mixed_float_multiplication",
        LangNumber,
        None,
        4.5 * -2.3,
    )
