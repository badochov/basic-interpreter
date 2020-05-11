from basic import Basic
from lang_types.lang_number import LangNumber
from errors.invalid_syntax_error import InvalidSyntaxError


def test_wrong_syntax_multiplication() -> None:
    basic = Basic()

    [(res, err)] = basic.run(" let _ = 42*", "test_wrong_order_multiplication")
    assert err is not None
    assert res is None
    assert isinstance(err, InvalidSyntaxError)

    [(res, err)] = basic.run(" let _ = 42.5*", "test_wrong_order_multiplication_float")
    assert err is not None
    assert res is None
    assert isinstance(err, InvalidSyntaxError)

    [(res, err)] = basic.run(" let _ = *42", "test_wrong_order_multiplication")
    assert err is not None
    assert res is None
    assert isinstance(err, InvalidSyntaxError)

    [(res, err)] = basic.run(" let _ = *42.5", "test_wrong_order_multiplication_float")
    assert err is not None
    assert res is None
    assert isinstance(err, InvalidSyntaxError)


def test_integer_multiplication() -> None:
    basic = Basic()

    [(res, err)] = basic.run(" let _ = 4 * +2", "test_positive_integer_multiplication")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res._value == 4 * 2

    [(res, err)] = basic.run(" let _ = -4 * -2", "test_negative_integer_multiplication")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res._value == -4 * -2

    [(res, err)] = basic.run(" let _ = 4 * -2", "test_mixed_integer_multiplication")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res._value == 4 * -2


def test_float_multiplication() -> None:
    basic = Basic()

    [(res, err)] = basic.run(
        " let _ = 4.5 * +2.3", "test_positive_float_multiplication"
    )
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res._value == 4.5 * 2.3

    [(res, err)] = basic.run(
        " let _ = -4.5 * -2.3", "test_negative_float_multiplication"
    )
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res._value == -4.5 * -2.3

    [(res, err)] = basic.run(" let _ = 4.5 * -2.3", "test_mixed_float_multiplication")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res._value == 4.5 * -2.3
