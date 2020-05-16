from __future__ import annotations

from basic import Basic
from errors.invalid_syntax_error import InvalidSyntaxError
from errors.rt_error import RTError
from lang_types.lang_function import LangFunction
from lang_types.lang_number import LangNumber
from lang_types.lang_tuple import LangTuple
from lang_types.lang_variant_type import LangVariantType
from tests.utilities import run_test


def test_tuple_invalid_syntax() -> None:
    basic = Basic()

    run_test(basic, "let _ = ,", "test_tuple_invalid_syntax1", None, InvalidSyntaxError)
    run_test(
        basic, "let _ = ,1", "test_tuple_invalid_syntax2", None, InvalidSyntaxError
    )
    run_test(
        basic, "let _ = 1,,1", "test_tuple_invalid_syntax3", None, InvalidSyntaxError
    )
    run_test(basic, "let _ = 1,,", "test_tuple_valid_syntax4", None, InvalidSyntaxError)


def test_tuple_correct_syntax() -> None:
    basic = Basic()

    run_test(basic, "let _ = 1", "test_tuple_valid_syntax1", LangNumber, None)
    run_test(basic, "let _ = 1, 2", "test_tuple_valid_syntax2", LangTuple, None)
    run_test(basic, "let _ = 1, 2, 3", "test_tuple_valid_syntax3", LangTuple, None)
    run_test(basic, "let _ = (1, 2)", "test_tuple_valid_syntax4", LangTuple, None)


def test_unpacking() -> None:
    basic = Basic()
    run_test(basic, "let f, s = (1, 2)", "test_tuple_unpack1", LangTuple, None)
    run_test(basic, "f", "test_tuple_unpack2", LangNumber, None, 1)
    run_test(basic, "s", "test_tuple_unpack3", LangNumber, None, 2)


def test_pass_to_function() -> None:
    basic = Basic()

    run_test(
        basic, "let test tuple = []", "test_tuples_in_functions1", LangFunction, None
    )
    run_test(basic, "test (1, 2)", "test_tuples_in_functions2", LangVariantType, None)
    run_test(basic, "test (1 )", "test_tuples_in_functions3", LangVariantType, None)

    run_test(
        basic,
        "let fst (f, s) = f",
        "test_tuples_in_functions_destruct1",
        LangFunction,
        None,
    )
    run_test(basic, "fst (1 )", "test_tuples_in_functions_destruct2", None, RTError)
    run_test(
        basic, "fst (1, 2)", "test_tuples_in_functions_destruct3", LangNumber, None, 1
    )
    run_test(
        basic, "fst (2, 1)", "test_tuples_in_functions_destruct4", LangNumber, None, 2
    )

    run_test(
        basic,
        "let snd (f, s) = s",
        "test_tuples_in_functions_destruct2.1",
        LangFunction,
        None,
    )
    run_test(
        basic, "snd (1,2,3)", "test_tuples_in_functions_destruct2.2", None, RTError
    )
    run_test(
        basic, "snd (1, 2)", "test_tuples_in_functions_destruct2.3", LangNumber, None, 2
    )
    run_test(
        basic, "snd (2, 1)", "test_tuples_in_functions_destruct2.4", LangNumber, None, 1
    )
