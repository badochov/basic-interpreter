from basic import Basic
from lang_types.lang_number import LangNumber
from errors.invalid_syntax_error import InvalidSyntaxError


def test_wrong_syntax_if() -> None:
    basic = Basic()

    res, err = basic.run(" let _ = if", "test_wrong_syntax_if")
    assert err is not None
    assert res is None
    assert isinstance(err, InvalidSyntaxError)

    res, err = basic.run(" let _ = if 1 then 2", "test_wrong_syntax_if_float")
    assert err is not None
    assert res is None
    assert isinstance(err, InvalidSyntaxError)

    res, err = basic.run(" let _ = if 1 then 2 elif 3 then 2", "test_wrong_syntax_if")
    assert err is not None
    assert res is None
    assert isinstance(err, InvalidSyntaxError)

    res, err = basic.run(" let _ = if 1 2 else 4", "test_wrong_syntax_if_float")
    assert err is not None
    assert res is None
    assert isinstance(err, InvalidSyntaxError)

    res, err = basic.run(
        "let _ = if 1 then 2 else 4 elif 4 then 9", "test_wrong_syntax_if_float"
    )
    assert err is not None
    assert res is None
    assert isinstance(err, InvalidSyntaxError)

    res, err = basic.run(" let _ = 1 then 2 else", "test_wrong_syntax_if_float")
    assert err is not None
    assert res is None
    assert isinstance(err, InvalidSyntaxError)


def test_integer_if() -> None:
    basic = Basic()

    res, err = basic.run(" let _ = 4 != +2", "test_positive_integer_if")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == int(4 != 2)

    res, err = basic.run(" let _ = 4 != 4", "test_positive_integer_if_equals")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == int(4 != 4)

    res, err = basic.run(" let _ = -4 != -2", "test_negative_integer_if")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == int(-4 != -2)

    res, err = basic.run(" let _ = 4 != -2", "test_mixed_integer_if")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == int(4 != -2)


def test_if() -> None:
    basic = Basic()

    res, err = basic.run(" let _ = if 0 then 1 else 2", "test_if_just_else1")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == 2

    res, err = basic.run(" let _ = if 0 then 1 elif 1 then 2 else 3", "test_if_elif_1")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == 2

    res, err = basic.run(" let _ = if 0 then 1 elif 0 then 2 else 3", "test_if_elif_2")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == 3

    res, err = basic.run(
        "let _ = if 0 then 1 elif 0 then 2 elif 1 then 42 else 69",
        "test_if_multi_elif_1",
    )
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == 42

    res, err = basic.run(
        "let _ = if 0 then 1 elif 0 then 2 elif 0 then 42 else 69",
        "test_if_multi_elif_2",
    )
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == 69

    res, err = basic.run(
        "let _ = if 0 then 1 elif 0 then 2 else if 1 then 42 else 69",
        "test_if_nested_if_1",
    )
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == 42

    res, err = basic.run(
        "let _ = if 0 then 1 elif 0 then 2 else if 0 then 42 else 69",
        "test_if_nested_if_2",
    )
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == 69
