from __future__ import annotations

from basic import Basic
from errors.invalid_syntax_error import InvalidSyntaxError
from lang_types.lang_function import LangFunction
from lang_types.lang_variant_type import LangVariantType
from tests.utilities import run_test


def test_list_invalid_syntax() -> None:
    basic = Basic()

    run_test(basic, "let _ = ][", "test_list_invalid_syntax1", None, InvalidSyntaxError)
    run_test(
        basic, "let _ = [1 2]", "test_list_invalid_syntax2", None, InvalidSyntaxError
    )
    run_test(
        basic, "let _ = [1, 2,,]", "test_list_invalid_syntax3", None, InvalidSyntaxError
    )
    run_test(basic, "let _ = [,]", "test_list_valid_syntax4", None, InvalidSyntaxError)


def test_list_correct_syntax() -> None:
    basic = Basic()

    run_test(basic, "let _ = []", "test_list_valid_syntax1", LangVariantType, None)
    run_test(basic, "let _ = [1,2,3]", "test_list_valid_syntax2", LangVariantType, None)
    run_test(basic, "let _ = [1]", "test_list_valid_syntax3", LangVariantType, None)
    run_test(basic, "let _ = [1,]", "test_list_valid_syntax4", LangVariantType, None)


def test_pass_to_function() -> None:
    basic = Basic()

    run_test(
        basic, "let test list = []", "test_lists_in_functions1", LangFunction, None
    )
    run_test(basic, "test []", "test_lists_in_functions2", LangVariantType, None)
    run_test(basic, "test ([])", "test_lists_in_functions2", LangVariantType, None)
