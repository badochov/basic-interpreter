from basic import Basic
from errors.invalid_syntax_error import InvalidSyntaxError
from lang_types.lang_bool import LangBool
from lang_types.lang_number import LangNumber
from tests.utilities import run_test


def test_wrong_syntax_if() -> None:
    basic = Basic()

    run_test(basic, " let _ = if", "test_wrong_syntax_if", None, InvalidSyntaxError)
    run_test(
        basic,
        " let _ = if 1 then 2",
        "test_wrong_syntax_if_float",
        None,
        InvalidSyntaxError,
    )
    run_test(
        basic,
        " let _ = if 1 then 2 elif 3 then 2",
        "test_wrong_syntax_if",
        None,
        InvalidSyntaxError,
    )
    run_test(
        basic,
        " let _ = if 1 2 else 4",
        "test_wrong_syntax_if_float",
        None,
        InvalidSyntaxError,
    )
    run_test(
        basic,
        "let _ = if 1 then 2 else 4 elif 4 then 9",
        "test_wrong_syntax_if_float",
        None,
        InvalidSyntaxError,
    )
    run_test(
        basic,
        " let _ = 1 then 2 else",
        "test_wrong_syntax_if_float",
        None,
        InvalidSyntaxError,
    )


def test_integer_equals() -> None:
    basic = Basic()

    run_test(
        basic,
        " let _ = 4 != +2",
        "test_positive_integer_equals",
        LangBool,
        None,
        4 != 2,
    )
    run_test(
        basic,
        " let _ = 4 != 4",
        "test_positive_integer_not_equals",
        LangBool,
        None,
        (4 != 4),
    )
    run_test(
        basic,
        " let _ = -4 != -2",
        "test_negative_integer_not_equals",
        LangBool,
        None,
        (-4 != -2),
    )
    run_test(
        basic,
        " let _ = 4 != -2",
        "test_mixed_integer_not_equals",
        LangBool,
        None,
        (4 != -2),
    )


def test_if() -> None:
    basic = Basic()

    run_test(
        basic,
        " let _ = if false then 1 else 2",
        "test_if_just_else1",
        LangNumber,
        None,
        2,
    )
    run_test(
        basic,
        " let _ = if false then 1 elif true then 2 else 3",
        "test_if_elif_1",
        LangNumber,
        None,
        2,
    )
    run_test(
        basic,
        " let _ = if false then 1 elif false then 2 else 3",
        "test_if_elif_2",
        LangNumber,
        None,
        3,
    )
    run_test(
        basic,
        "let _ = if false then 1 elif false then 2 elif true then 42 else 69",
        "test_if_multi_elif_1",
        LangNumber,
        None,
        42,
    )
    run_test(
        basic,
        "let _ = if false then 1 elif false then 2 elif false then 42 else 69",
        "test_if_multi_elif_2",
        LangNumber,
        None,
        69,
    )
    run_test(
        basic,
        "let _ = if false then 1 elif false then 2 else if true then 42 else 69",
        "test_if_nested_if_1",
        LangNumber,
        None,
        42,
    )
    run_test(
        basic,
        "let _ = if false then 1 elif false then 2 else if false then 42 else 69",
        "test_if_nested_if_2",
        LangNumber,
        None,
        69,
    )
