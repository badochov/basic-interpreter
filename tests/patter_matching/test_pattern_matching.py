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
        basic, "match a with Some b -> 1", "no end",
    )
    run_test_invalid_syntax_error(
        basic, "match a Some b -> 1 end", "no with",
    )
    run_test_invalid_syntax_error(basic, "a with Some b -> b end", "no end")


def test_mismatch() -> None:
    basic = Basic()

    run_test_rt_error(basic, "match [] with Some a -> a end", "no_match")

    run_test_rt_error(
        basic, "match Some a with Some a b -> a end", "incorrect_arg_count"
    )
    run_test_rt_error(
        basic, "let a, *,c, b = (1, 2)", "tuple_arg_count_mismatch2",
    )


def test_correct_unpacking() -> None:
    basic = Basic()

    run_test_correct(
        basic, "match [] with Empty -> 0 end", "correct_unpacking1", [LangNumber], [0],
    )
    run_test_correct(
        basic,
        "match [1] with Empty -> 0 | List l tail -> l end",
        "correct_unpacking1",
        [LangNumber],
        [1],
    )
    run_test_correct(
        basic,
        "match [[1]] with Empty -> 0 | List (List l _) _ -> l end",
        "correct_unpacking1",
        [LangNumber],
        [1],
    )
