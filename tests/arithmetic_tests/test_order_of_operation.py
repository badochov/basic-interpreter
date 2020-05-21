from basic import Basic
from errors.invalid_syntax_error import InvalidSyntaxError
from lang_types.lang_number import LangNumber
from tests.utilities import run_test


def test_parentheses() -> None:
    basic = Basic()

    run_test(
        basic, " let _ = (4 + 2)", "test_single_parentheses", LangNumber, None, (4 + 2)
    )
    run_test(
        basic, " let _ = (4) + 2", "test_single_parentheses", LangNumber, None, (4) + 2
    )
    run_test(
        basic,
        " let _ = ((4 + 2) + 6)",
        "test_double_parentheses",
        LangNumber,
        None,
        ((4 + 2) + 6),
    )
    run_test(
        basic,
        " let _ = -((4 + 2) + 6)",
        "test_double_parentheses_negation",
        LangNumber,
        None,
        -((4 + 2) + 6),
    )


def test_parentheses_error() -> None:
    basic = Basic()

    run_test(
        basic,
        " let _ = (4 + 2",
        "test_unclosed_parentheses_error",
        None,
        InvalidSyntaxError,
    )
    run_test(
        basic,
        " let _ = 4 + 2)",
        "test_unopened_parentheses_error",
        None,
        InvalidSyntaxError,
    )
    run_test(
        basic,
        " let _ = (4 +) 2",
        "test_wrong_parentheses_placement",
        None,
        InvalidSyntaxError,
    )


def test_order() -> None:
    basic = Basic()

    run_test(
        basic, " let _ = 42 - 6 * 7", "test_order_-2", LangNumber, None, 42 - 6 * 7
    )
    run_test(
        basic,
        " let _ = 7 + 2 * (6 + 3) / 3 - 7",
        "test_order_-1",
        LangNumber,
        None,
        7 + 2 * (6 + 3) / 3 - 7,
    )
    run_test(basic, " let _ = 42 - 6 * 7", "test_order_0", LangNumber, None, 42 - 6 * 7)
    run_test(
        basic,
        " let _ = 7 + 2 * (6 + 3) / 3 - 7",
        "test_order_1",
        LangNumber,
        None,
        7 + 2 * (6 + 3) / 3 - 7,
    )
    run_test(basic, " let _ = 42 - 6 * 7", "test_order_2", LangNumber, None, 42 - 6 * 7)
    run_test(
        basic, " let _ = 11 + 19 * 2", "test_order_3", LangNumber, None, 11 + 19 * 2
    )
    run_test(basic, " let _ = 42 - 6 * 7", "test_order_4", LangNumber, None, 42 - 6 * 7)
    run_test(
        basic,
        " let _ = 7 + 2 * (6 + 3) / 3 - 7",
        "test_order_5",
        LangNumber,
        None,
        7 + 2 * (6 + 3) / 3 - 7,
    )
    run_test(
        basic,
        " let _ = (14 + 2) * 2 + 3",
        "test_order_6",
        LangNumber,
        None,
        (14 + 2) * 2 + 3,
    )
    run_test(
        basic,
        " let _ = 120 / (6 + 12 * 2)",
        "test_order_7",
        LangNumber,
        None,
        120 / (6 + 12 * 2),
    )
    run_test(
        basic, " let _ = 12 + 2 * 44", "test_order_8", LangNumber, None, 12 + 2 * 44
    )
    run_test(
        basic,
        " let _ = 10 * 2 - (7 + 9)",
        "test_order_9",
        LangNumber,
        None,
        10 * 2 - (7 + 9),
    )
    run_test(basic, " let _ = 2 * 2 ^ 3", "test_order_10", LangNumber, None, 2 * 2 ** 3)
    run_test(
        basic,
        " let _ = 2 * 2 ^ 3 * 2",
        "test_order_11",
        LangNumber,
        None,
        2 * 2 ** 3 * 2,
    )
