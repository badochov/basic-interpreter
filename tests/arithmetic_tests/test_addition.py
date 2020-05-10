from basic import Basic
from errors.invalid_syntax_error import InvalidSyntaxError
from lang_types.lang_number import LangNumber


def test_pos_number() -> None:
    basic = Basic()

    res, err = basic.run(" let _ = +42", "test_pos_integer")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res._value == 42

    res, err = basic.run(" let _ = +42.5", "test_pos_float")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res._value == 42.5


def test_integer_addition() -> None:
    basic = Basic()

    res, err = basic.run(" let _ = 4 + 2", "test_positive_integer_addition")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res._value == 6

    res, err = basic.run(" let _ = -4 + -2", "test_negative_integer_addition")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res._value == -6

    res, err = basic.run(" let _ = 4 + -2", "test_mixed_integer_addition")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res._value == 2


def test_float_addition() -> None:
    basic = Basic()

    res, err = basic.run(" let _ = 4.5 + 2.3", "test_positive_float_addition")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res._value == 4.5 + 2.3

    res, err = basic.run(" let _ = -4.5 + -2.3", "test_negative_float_addition")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res._value == -4.5 + -2.3

    res, err = basic.run(" let _ = 4.5 + -2.3", "test_mixed_float_addition")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res._value == 4.5 + -2.3


def test_invalid_syntax_addition() -> None:
    basic = Basic()

    res, err = basic.run(" let _ = 42+", "test_wrong_syntax_int")
    assert err is not None
    assert res is None
    assert isinstance(err, InvalidSyntaxError)

    res, err = basic.run(" let _ = 42.5+", "test_wrong_syntax_float")
    assert err is not None
    assert res is None
    assert isinstance(err, InvalidSyntaxError)
