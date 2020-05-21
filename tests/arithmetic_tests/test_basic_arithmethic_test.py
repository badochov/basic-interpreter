from basic import Basic
from errors.invalid_syntax_error import InvalidSyntaxError
from lang_types.lang_number import LangNumber
from tests.utilities import run_test

OPERATORS = {
    "addition": "+",
    "subtraction": "-",
    "division": "/",
    "multiplication": "*",
    "power": "^",
}


def test_wrong_arithmetic_operator() -> None:
    basic = Basic()
    for name, operator in OPERATORS.items():
        run_test(
            basic,
            " let _ = 42" + operator,
            "test_wrong_order_" + name,
            None,
            InvalidSyntaxError,
        )
        run_test(
            basic,
            " let _ = 42.5" + operator,
            "test_wrong_order_" + name + "_float",
            None,
            InvalidSyntaxError,
        )


def py_op(op: str) -> str:
    return "**" if op == "^" else op


def test_integer_arithmetic_operator() -> None:
    basic = Basic()

    for name, operator in OPERATORS.items():
        run_test(
            basic,
            " let _ = 4 " + operator + " +2",
            "test_positive_integer" + name,
            LangNumber,
            None,
            (eval("4 " + py_op(operator) + " +2")),
        )
        run_test(
            basic,
            " let _ = -4 " + operator + " -2",
            "test_positive_integer_" + name,
            LangNumber,
            None,
            (eval("-4 " + py_op(operator) + " -2")),
        )
        run_test(
            basic,
            " let _ = 4 " + operator + " -2",
            "test_negative_" + name,
            LangNumber,
            None,
            (eval("4 " + py_op(operator) + " -2")),
        )


def test_float_arithmetic_operator() -> None:
    basic = Basic()

    for name, operator in OPERATORS.items():
        run_test(
            basic,
            " let _ = 4.5 " + operator + " +2.3",
            "test_positive_float_" + name,
            LangNumber,
            None,
            (eval("4.5 " + py_op(operator) + " +2.3")),
        )
        run_test(
            basic,
            " let _ = -4.5 " + operator + " -2.3",
            "test_negative_float_" + name,
            LangNumber,
            None,
            (eval("-4.5 " + py_op(operator) + " -2.3")),
        )
        run_test(
            basic,
            " let _ = -4.5 " + operator + " -4.5",
            "test_negative_float_2_" + name,
            LangNumber,
            None,
            (eval("-4.5 " + py_op(operator) + " -4.5")),
        )
        run_test(
            basic,
            " let _ = 4.5 " + operator + " -2.3",
            "test_mixed_float_" + name,
            LangNumber,
            None,
            (eval("4.5 " + py_op(operator) + " -2.3")),
        )


def test_mixed_arithmetic_operator() -> None:
    basic = Basic()

    for name, operator in OPERATORS.items():
        run_test(
            basic,
            " let _ = 4.5 " + operator + " +5",
            "test_positive_mixed_" + name,
            LangNumber,
            None,
            (eval("4.5 " + py_op(operator) + " +5")),
        )
        run_test(
            basic,
            " let _ = -4.5 " + operator + " -2",
            "test_negative_mixed_" + name,
            LangNumber,
            None,
            (eval("-4.5 " + py_op(operator) + " -2")),
        )
        run_test(
            basic,
            " let _ = -4.0 " + operator + " -4",
            "test_negative_mixed_" + name,
            LangNumber,
            None,
            (eval("-4.0 " + py_op(operator) + " -4")),
        )
