from basic import Basic
from lang_types.lang_number import LangNumber
from errors.invalid_syntax_error import InvalidSyntaxError
from tests.utilities import run_test


def test_wrong_syntax_raise_to_power() -> None:
    basic = Basic()

    run_test(
        basic,
        " let _ = 42^",
        "test_wrong_order_raise_to_power",
        None,
        InvalidSyntaxError,
    )
    run_test(
        basic,
        " let _ = 42.5^",
        "test_wrong_order_raise_to_power_float",
        None,
        InvalidSyntaxError,
    )
    run_test(
        basic,
        " let _ = ^42",
        "test_wrong_order_raise_to_power",
        None,
        InvalidSyntaxError,
    )
    run_test(
        basic,
        " let _ = ^42.5",
        "test_wrong_order_raise_to_power_float",
        None,
        InvalidSyntaxError,
    )


def test_integer_raise_to_power() -> None:
    basic = Basic()

    run_test(
        basic,
        " let _ = 4 ^ +2",
        "test_positive_integer_raise_to_power",
        LangNumber,
        None,
        4 ** 2,
    )
    run_test(
        basic,
        " let _ = -4 ^ -2",
        "test_negative_integer_raise_to_power",
        LangNumber,
        None,
        -(4 ** -2),
    )
    run_test(
        basic,
        " let _ = 4 ^ -2",
        "test_mixed_integer_raise_to_power",
        LangNumber,
        None,
        4 ** -2,
    )


def test_float_raise_to_power() -> None:
    basic = Basic()

    run_test(
        basic,
        " let _ = 4.5 ^ +2.3",
        "test_positive_float_raise_to_power",
        LangNumber,
        None,
        4.5 ** 2.3,
    )
    run_test(
        basic,
        " let _ = -4.5 ^ -2.3",
        "test_negative_float_raise_to_power",
        LangNumber,
        None,
        -(4.5 ** -2.3),
    )
    run_test(
        basic,
        "let _ = 4.5 ^ -2.3",
        "test_mixed_float_raise_to_power",
        LangNumber,
        None,
        4.5 ** -2.3,
    )


def test_negation_raise_to_power() -> None:
    basic = Basic()

    run_test(
        basic,
        "let _ = -4.5 ^ +2",
        "test_negation_not_in_parentheses_raised_to_power",
        LangNumber,
        None,
        -(4.5 ** 2),
    )
    run_test(
        basic,
        " let _ = (-4.5) ^ 2",
        "test_negation_in_parentheses_raised_to_power",
        LangNumber,
        None,
        (-4.5) ** +2,
    )
