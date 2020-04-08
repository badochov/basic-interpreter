from basic import Basic
from lang_types.lang_number import LangNumber
from errors.unexpected_char_error import UnexpectedCharError
from errors.invalid_syntax_error import InvalidSyntaxError


def test_negation() -> None:
    basic = Basic()

    res, err = basic.run(" let _ = -42", "test_single_negation")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == -42

    res, err = basic.run(" let _ = --42", "test_double_negation")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == 42

    res, err = basic.run(" let _ = -42.5", "test_single_negation_float")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == -42.5

    res, err = basic.run(" let _ = --42.5", "test_double_negation_float")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == 42.5


def test_wrong_syntax() -> None:
    basic = Basic()

    res, err = basic.run(" let _ = 42-", "test_wrong_order_negation")
    assert err is not None
    assert res is None
    assert isinstance(err, InvalidSyntaxError)

    res, err = basic.run(" let _ = 42.5-", "test_wrong_order_negation_float")
    assert err is not None
    assert res is None
    assert isinstance(err, InvalidSyntaxError)


def test_integer_subtraction() -> None:
    basic = Basic()

    res, err = basic.run(" let _ = 4 - +2", "test_positive_integer_subtraction")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == 4 - 2

    res, err = basic.run(" let _ = -4 - -2", "test_negative_integer_subtraction")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == -4 - -2

    res, err = basic.run(" let _ = 4 - -2", "test_mixed_integer_subtraction")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == 4 - -2


def test_float_subtraction() -> None:
    basic = Basic()

    res, err = basic.run(" let _ = 4.5 - +2.3", "test_positive_float_subtraction")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == 4.5 - 2.3

    res, err = basic.run(" let _ = -4.5 - -2.3", "test_negative_float_subtraction")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == -4.5 - -2.3

    res, err = basic.run(" let _ = 4.5 - -2.3", "test_mixed_float_subtraction")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == 4.5 - -2.3
