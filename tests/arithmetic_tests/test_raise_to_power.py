from basic import Basic
from lang_types.lang_number import LangNumber
from errors.invalid_syntax_error import InvalidSyntaxError


def test_wrong_syntax_raise_to_power() -> None:
    basic = Basic()

    res, err = basic.run(" let _ = 42^", "test_wrong_order_raise_to_power")
    assert err is not None
    assert res is None
    assert isinstance(err, InvalidSyntaxError)

    res, err = basic.run(" let _ = 42.5^", "test_wrong_order_raise_to_power_float")
    assert err is not None
    assert res is None
    assert isinstance(err, InvalidSyntaxError)

    res, err = basic.run(" let _ = ^42", "test_wrong_order_raise_to_power")
    assert err is not None
    assert res is None
    assert isinstance(err, InvalidSyntaxError)

    res, err = basic.run(" let _ = ^42.5", "test_wrong_order_raise_to_power_float")
    assert err is not None
    assert res is None
    assert isinstance(err, InvalidSyntaxError)


def test_integer_raise_to_power() -> None:
    basic = Basic()

    res, err = basic.run(" let _ = 4 ^ +2", "test_positive_integer_raise_to_power")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == 4 ** 2

    res, err = basic.run(" let _ = -4 ^ -2", "test_negative_integer_raise_to_power")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == -(4 ** -2)

    res, err = basic.run(" let _ = 4 ^ -2", "test_mixed_integer_raise_to_power")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == 4 ** -2


def test_float_raise_to_power() -> None:
    basic = Basic()

    res, err = basic.run(" let _ = 4.5 ^ +2.3", "test_positive_float_raise_to_power")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == 4.5 ** 2.3

    res, err = basic.run(" let _ = -4.5 ^ -2.3", "test_negative_float_raise_to_power")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == -(4.5 ** -2.3)

    res, err = basic.run("let _ = 4.5 ^ -2.3", "test_mixed_float_raise_to_power")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == 4.5 ** -2.3


def test_negation_raise_to_power() -> None:
    basic = Basic()

    res, err = basic.run(
        "let _ = -4.5 ^ +2", "test_negation_not_in_parentheses_raised_to_power"
    )
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == -(4.5 ** 2)

    res, err = basic.run(
        " let _ = (-4.5) ^ 2", "test_negation_in_parentheses_raised_to_power"
    )
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == (-4.5) ** +2
