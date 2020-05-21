from basic import Basic
from lang_types.lang_bool import LangBool
from lang_types.lang_number import LangNumber
from lang_types.lang_tuple import LangTuple
from lang_types.lang_variant_type import LangVariantType
from tests.utilities import (
    run_test_correct,
    run_test_rt_error,
    run_test_invalid_syntax_error,
)


def test_incorrect_syntax() -> None:
    basic = Basic()

    run_test_invalid_syntax_error(
        basic, "let a, *args = (1, 2)", "tuple_group_with_name",
    )
    run_test_invalid_syntax_error(basic, "let a [a, (b, _])", "random_invalid_syntax")


def test_mismatch() -> None:
    basic = Basic()

    run_test_rt_error(basic, "let a, b = (1, 2, 3)", "tuple_arg_count_mismatch")

    run_test_rt_error(basic, "let a, * = 1", "tuple_type_mismatch")
    run_test_rt_error(
        basic, "let a, *,c, b = (1, 2)", "tuple_arg_count_mismatch2",
    )
    run_test_rt_error(basic, "let (a, [b]) = (1, 2)", "list_type_mismatch")
    run_test_rt_error(basic, "let [(a, b)] = [1, 2]", "tuple_type_mismatch")
    run_test_rt_error(basic, "let a, b, c = 1, (2, 3)", "tuple_type_mismatch")
    run_test_rt_error(basic, "let a, (b, c) = 1, 2, 3", "tuple_type_mismatch")


def test_correct_unpacking() -> None:
    basic = Basic()

    run_test_correct(
        basic,
        "let a, b = 1, 2 a == 1 b == 2",
        "correct_unpacking1",
        [LangTuple, LangBool, LangBool],
        [..., True, True],
    )
    run_test_correct(
        basic,
        "let a, b, c = 1, 2, 3 a == 1 b == 2, c == 3",
        "correct_unpacking2",
        [LangTuple, LangBool, LangBool, LangBool],
        [..., True, True, True],
    )
    run_test_correct(
        basic,
        "let a, (b, c) = 1, (2, 3) a == 1 b == 2, c == 3",
        "correct_unpacking3",
        [LangTuple, LangBool, LangBool, LangBool],
        [..., True, True, True],
    )
    run_test_correct(
        basic,
        "let a, (b, (c, d)) = 1, (2, (3, 4)) a == 1 b == 2, c == 3 d == 4",
        "correct_unpacking4",
        [LangTuple, LangBool, LangBool, LangBool, LangBool],
        [..., True, True, True, True],
    )
    run_test_correct(
        basic,
        "let a, * = 1, 2, 3 a == 1",
        "correct_unpacking4",
        [LangTuple, LangBool],
        [..., True],
    )
    run_test_correct(
        basic,
        "let a, b, * = 1, 2, 3 a == 1 b == 2",
        "correct_unpacking5",
        [LangTuple, LangBool, LangBool],
        [..., True, True],
    )
    run_test_correct(
        basic,
        "let *, a = 1, 2, 3 a == 3",
        "correct_unpacking6",
        [LangTuple, LangBool],
        [..., True],
    )
    run_test_correct(
        basic,
        "let *, a, b = 1, 2, 3 a == 2 b == 3",
        "correct_unpacking7",
        [LangTuple, LangBool, LangBool],
        [..., True, True],
    )
    run_test_correct(
        basic,
        "let a, *, b = 1, 2, 3 a == 3",
        "correct_unpacking8",
        [LangTuple, LangBool],
        [..., True],
    )
    run_test_correct(
        basic,
        "let a, b, *, c, d = 1, 2, 3, 4, 5 a == 1 b == 2 c == 4 d == 5",
        "correct_unpacking9",
        [LangTuple, LangBool, LangBool, LangBool, LangBool],
        [..., True, True, True, True],
    )
    run_test_correct(
        basic,
        "let a, b, *, c, d = 1, 2, 4, 5 a == 1 b == 2 c == 4 d == 5",
        "correct_unpacking10",
        [LangTuple, LangBool, LangBool, LangBool, LangBool],
        [..., True, True, True, True],
    )
    run_test_correct(
        basic,
        "let a, b, *, c, d = 1, 2, 3, 3, 4, 5 a == 1 b == 2 c == 4 d == 5",
        "correct_unpacking10",
        [LangTuple, LangBool, LangBool, LangBool, LangBool],
        [..., True, True, True, True],
    )
    run_test_correct(
        basic,
        "let (a, b), *, (c, d) = (1, 2), 3, 3, (4, 5) a == 1 b == 2 c == 4 d == 5",
        "correct_unpacking10",
        [LangTuple, LangBool, LangBool, LangBool, LangBool],
        [..., True, True, True, True],
    )
    run_test_correct(
        basic,
        "let [a] == [1] a == 1",
        "correct_unpacking11",
        [LangVariantType, LangBool],
        [..., 1],
    )
    run_test_correct(
        basic,
        "let [a, [b]] == [1, [2]] a == 1 b == 2",
        "correct_unpacking12",
        [LangVariantType, LangBool, LangBool],
        [..., 1, 2],
    )
    run_test_correct(
        basic,
        "let [a, *b] == [1, 2, 3] a == 1 b",
        "correct_unpacking13",
        [LangVariantType, LangBool, LangVariantType],
        [..., 1, ...],
    )
    run_test_correct(
        basic,
        "let [a, (b, c)] = [1, (2, 3)] (a) (b) (c)",
        "correct_unpacking14",
        [LangVariantType, LangNumber, LangNumber, LangNumber],
        [..., 1, 2, 3],
    )
    run_test_correct(
        basic,
        "let (a, [b, c]) = (1, [2, 3]) (a) (b) (c)",
        "correct_unpacking15",
        [LangVariantType, LangNumber, LangNumber, LangNumber],
        [..., 1, 2, 3],
    )
