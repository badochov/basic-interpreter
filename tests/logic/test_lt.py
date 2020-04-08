from basic import Basic
from lang_types.lang_number import LangNumber
from errors.invalid_syntax_error import InvalidSyntaxError


def test_wrong_syntax_less_than() -> None:
    basic = Basic()

    res, err = basic.run(" let _ = 42<", "test_wrong_order_less_than")
    assert err is not None
    assert res is None
    assert isinstance(err, InvalidSyntaxError)

    res, err = basic.run(" let _ = 42.5<", "test_wrong_order_less_than_float")
    assert err is not None
    assert res is None
    assert isinstance(err, InvalidSyntaxError)

    res, err = basic.run(" let _ = <42", "test_wrong_order_less_than")
    assert err is not None
    assert res is None
    assert isinstance(err, InvalidSyntaxError)

    res, err = basic.run(" let _ = <42.5", "test_wrong_order_less_than_float")
    assert err is not None
    assert res is None
    assert isinstance(err, InvalidSyntaxError)


def test_integer_less_than() -> None:
    basic = Basic()

    res, err = basic.run(" let _ = 4 < +2", "test_positive_integer_less_than")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == int(4 < 2)

    res, err = basic.run(" let _ = 4 < 4", "test_positive_integer_less_than_equals")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == int(4 < 4)

    res, err = basic.run(" let _ = -4 < -2", "test_negative_integer_less_than")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == int(-4 < -2)

    res, err = basic.run(" let _ = 4 < -2", "test_mixed_integer_less_than")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == int(4 < -2)


def test_float_less_than() -> None:
    basic = Basic()

    res, err = basic.run(" let _ = 4.5 < +2.3", "test_positive_float_less_than")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == int(4.5 < 2.3)

    res, err = basic.run(" let _ = 4.5 < 4.5", "test_positive_float_less_than_equals")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == int(4.5 < 4.5)

    res, err = basic.run(" let _ = -4.5 < -2.3", "test_negative_float_less_than")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == int(-4.5 < -2.3)

    res, err = basic.run(" let _ = 4.5 < -2.3", "test_mixed_float_less_than")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == int(4.5 < -2.3)


def test_mixed_less_than() -> None:
    basic = Basic()

    res, err = basic.run(" let _ = 4.5 < 5", "test_positive_float_less_than")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == int(4.5 < 5)

    res, err = basic.run(" let _ = -4.5 < -2", "test_negative_float_less_than")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == int(-4.5 < -2)

    res, err = basic.run(" let _ = -4.0 < -4", "test_negative_miged_less_than_equals")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == int(-4.0 < -4)
