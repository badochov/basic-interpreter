from basic import Basic
from lang_types.lang_number import LangNumber
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
