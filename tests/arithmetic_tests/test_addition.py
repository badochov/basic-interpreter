from __future__ import annotations

from basic import Basic
from errors.invalid_syntax_error import InvalidSyntaxError
from lang_types.lang_number import LangNumber
from tests.utilities import run_test


def test_pos_number() -> None:
    basic = Basic()

    run_test(basic, "let _ = 42", "test_pos_integer", LangNumber, None, 42)
    run_test(basic, "let _ = +42.5", "test_pos_float", LangNumber, None, 42.5)


def test_integer_addition() -> None:
    basic = Basic()

    run_test(
        basic, " let _ = 4 + 2", "test_positive_integer_addition", LangNumber, None, 6
    )
    run_test(
        basic, " let _ = -4 + -2", "test_negative_int_addition", LangNumber, None, -6,
    )
    run_test(
        basic, " let _ = 4 + -2", "test_mixed_integer_addition", LangNumber, None, 2
    )


def test_float_addition() -> None:
    basic = Basic()

    run_test(
        basic,
        " let _ = 4.5 + 2.3",
        "test_positive_float_add",
        LangNumber,
        None,
        4.5 + 2.3,
    )
    run_test(
        basic,
        "let _ = -4.5 + -2.3",
        "test_neg_float_add",
        LangNumber,
        None,
        -4.5 + -2.3,
    )

    run_test(
        basic,
        " let _ = 4.5 + -2.3",
        "test_mixed_float_add",
        LangNumber,
        None,
        4.5 - 2.3,
    )


def test_invalid_syntax_addition() -> None:
    basic = Basic()

    run_test(basic, " let _ = 42+", "test_wrong_syntax_int", None, InvalidSyntaxError)

    run_test(
        basic, " let _ = 42.5+", "test_wrong_syntax_float", None, InvalidSyntaxError
    )
