from basic import Basic
from lang_types.lang_number import LangNumber
from errors.unexpected_char_error import UnexpectedCharError
from errors.invalid_syntax_error import InvalidSyntaxError
from tests.utilities import run_test


def test_negation() -> None:
    basic = Basic()

    run_test(basic, " let _ = -42", "test_single_negation", LangNumber, None, -42)
    run_test(basic, " let _ = --42", "test_double_negation", LangNumber, None, 42)
    run_test(
        basic, " let _ = -42.5", "test_single_negation_float", LangNumber, None, -42.5
    )
    run_test(
        basic, " let _ = --42.5", "test_double_negation_float", LangNumber, None, 42.5
    )


def test_wrong_syntax() -> None:
    basic = Basic()

    run_test(
        basic, " let _ = 42-", "test_wrong_order_negation", None, InvalidSyntaxError
    )
    run_test(
        basic,
        " let _ = 42.5-",
        "test_wrong_order_negation_float",
        None,
        InvalidSyntaxError,
    )


def test_integer_subtraction() -> None:
    basic = Basic()

    run_test(
        basic,
        " let _ = 4 - +2",
        "test_positive_integer_subtraction",
        LangNumber,
        None,
        4 - 2,
    )
    run_test(
        basic,
        " let _ = -4 - -2",
        "test_negative_integer_subtraction",
        LangNumber,
        None,
        -4 - -2,
    )
    run_test(
        basic,
        " let _ = 4 - -2",
        "test_mixed_integer_subtraction",
        LangNumber,
        None,
        4 - -2,
    )


def test_float_subtraction() -> None:
    basic = Basic()

    run_test(
        basic,
        " let _ = 4.5 - +2.3",
        "test_positive_float_subtraction",
        LangNumber,
        None,
        4.5 - 2.3,
    )
    run_test(
        basic,
        " let _ = -4.5 - -2.3",
        "test_negative_float_subtraction",
        LangNumber,
        None,
        -4.5 - -2.3,
    )
    run_test(
        basic,
        " let _ = 4.5 - -2.3",
        "test_mixed_float_subtraction",
        LangNumber,
        None,
        4.5 - -2.3,
    )
