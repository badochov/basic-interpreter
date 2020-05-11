from basic import Basic
from errors.invalid_syntax_error import InvalidSyntaxError
from errors.rt_error import RTError
from lang_types.lang_number import LangNumber
from tests.utilities import run_test


def test_wrong_syntax_assignment() -> None:
    basic = Basic()

    run_test(
        basic, "a let 0 =", "test_wrong_order_assignment", None, InvalidSyntaxError
    )
    run_test(
        basic, "a let = 0", "test_wrong_order_assignment_2", None, InvalidSyntaxError
    )
    run_test(
        basic, "0 = let a", "test_wrong_order_assignment_3", None, InvalidSyntaxError
    )
    run_test(
        basic, "= 0 let a", "test_wrong_order_assignment_4", None, InvalidSyntaxError
    )
    run_test(
        basic,
        "1 + let a = 0",
        "test_wrong_order_assignment_5",
        None,
        InvalidSyntaxError,
    )


def test_integer_assignment() -> None:
    basic = Basic()

    run_test(
        basic, "let a1 = 0", "test_positive_integer_assignment", LangNumber, None, 0
    )
    run_test(
        basic, "let a2 = -2", "test_negative_integer_assignment", LangNumber, None, -2
    )
    run_test(
        basic,
        "let a3 = 2 + 2",
        "test_addition_integer_assignment_part1",
        LangNumber,
        None,
        4,
    )
    run_test(
        basic,
        "let _ = a3",
        "test_addition_integer_assignment_part2",
        LangNumber,
        None,
        4,
    )
    run_test(
        basic,
        "let a4 = 2 + 2",
        "test_multiplication_integer_assignment_part1",
        LangNumber,
        None,
        4,
    )
    run_test(
        basic,
        "let _ = a4",
        "test_multiplication_integer_assignment_part2",
        LangNumber,
        None,
        4,
    )
    run_test(
        basic,
        "let a5 = 2 ^ 2",
        "test_raised_to_power_integer_assignment_part1",
        LangNumber,
        None,
        4,
    )
    run_test(
        basic,
        "let _ = a5",
        "test_raised_to_power_integer_assignment_part2",
        LangNumber,
        None,
        4,
    )
    run_test(
        basic,
        "let a6 = (let a7 = 2 in a7) * (let a8 = 1 in a8) * (let a9 = 3 in a9) * (let a10 = 7 in a10)",
        "test_assignement_output_part1",
        LangNumber,
        None,
        2 * 1 * 3 * 7,
    )
    run_test(
        basic,
        "let _ = a6",
        "test_assignement_output_part2",
        LangNumber,
        None,
        2 * 1 * 3 * 7,
    )
    run_test(basic, "let _ = a7", "test_assignement_output_part3", LangNumber, None, 2)
    run_test(basic, "let _ = a8", "test_assignement_output_part4", LangNumber, None, 1)
    run_test(basic, "let _ = a9", "test_assignement_output_part5", LangNumber, None, 3)
    run_test(basic, "let _ = a10", "test_assignement_output_part6", LangNumber, None, 7)
    run_test(
        basic,
        "let a11 = (let a12 = 2 in a12)",
        "test_multi_assignement_part1",
        LangNumber,
        None,
        2,
    )
    run_test(basic, "let _ = a11", "test_multi_assignement_part2", LangNumber, None, 2)
    run_test(basic, "let _ = a12", "test_multi_assignement_part3", LangNumber, None, 2)


def test_float_assignment() -> None:
    basic = Basic()

    run_test(
        basic, "let a1 = 0.7", "test_positive_float_assignment", LangNumber, None, 0.7
    )
    run_test(
        basic, "let a2 = -0.7", "test_negative_float_assignment", LangNumber, None, -0.7
    )


def test_underscore_assignment() -> None:
    basic = Basic()

    run_test(
        basic, "let _ = 0.7", "test_underscore_assignment_part1", LangNumber, None, 0.7
    )
    run_test(basic, "_", "test_underscore_assignment_part2", None, RTError)
