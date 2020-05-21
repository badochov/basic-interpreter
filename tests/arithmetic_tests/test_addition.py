from __future__ import annotations

from basic import Basic
from lang_types.lang_number import LangNumber
from tests.utilities import run_test


def test_pos_number() -> None:
    basic = Basic()

    run_test(basic, "let _ = 42", "test_pos_integer", LangNumber, None, 42)
    run_test(basic, "let _ = +42.5", "test_pos_float", LangNumber, None, 42.5)
    run_test(basic, "let _ = ++42.5", "test_pos_float2", LangNumber, None, 42.5)
