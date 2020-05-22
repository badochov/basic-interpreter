from basic import Basic
from lang_types.lang_bool import LangBool
from lang_types.lang_number import LangNumber
from tests.utilities import run_test_correct, run_test_invalid_syntax_error


def test_wrong_syntax_if() -> None:
    basic = Basic()

    run_test_invalid_syntax_error(basic, "if", "test_wrong_syntax_if")
    run_test_invalid_syntax_error(basic, "if 1 then 2", "test_wrong_syntax_if_float")
    run_test_invalid_syntax_error(
        basic, "if 1 then 2 elif 3 then 2", "test_wrong_syntax_if"
    )
    run_test_invalid_syntax_error(basic, "if 1 2 else 4", "test_wrong_syntax_if_float")
    run_test_invalid_syntax_error(
        basic, "if 1 then 2 else 4 elif 4 then 9", "test_wrong_syntax_if_float"
    )
    run_test_invalid_syntax_error(basic, "1 then 2 else", "test_wrong_syntax_if_float")


def test_integer_equals() -> None:
    basic = Basic()

    run_test_correct(
        basic, s := "4 != +2", "test_positive_integer_equals", LangBool, eval(s),
    )
    run_test_correct(
        basic, s := "4 != 4", "test_positive_integer_not_equals", LangBool, eval(s),
    )
    run_test_correct(
        basic, s := "-4 != -2", "test_negative_integer_not_equals", LangBool, eval(s),
    )
    run_test_correct(
        basic, s := "4 != -2", "test_mixed_integer_not_equals", LangBool, eval(s),
    )


def test_if() -> None:
    basic = Basic()

    run_test_correct(
        basic, "if false then 1 else 2", "test_if_just_else1", LangNumber, 2
    )
    run_test_correct(
        basic,
        "if false then 1 elif true then 2 else 3",
        "test_if_elif_1",
        LangNumber,
        2,
    )
    run_test_correct(
        basic,
        "if false then 1 elif false then 2 else 3",
        "test_if_elif_2",
        LangNumber,
        3,
    )
    run_test_correct(
        basic,
        "if false then 1 elif false then 2 elif true then 42 else 69",
        "test_if_multi_elif_1",
        LangNumber,
        42,
    )
    run_test_correct(
        basic,
        "if false then 1 elif false then 2 elif false then 42 else 69",
        "test_if_multi_elif_2",
        LangNumber,
        69,
    )
    run_test_correct(
        basic,
        "let _ = if false then 1 elif false then 2 else if true then 42 else 69",
        "test_if_nested_if_1",
        LangNumber,
        42,
    )
    run_test_correct(
        basic,
        "let _ = if false then 1 elif false then 2 else if false then 42 else 69",
        "test_if_nested_if_2",
        LangNumber,
        69,
    )
