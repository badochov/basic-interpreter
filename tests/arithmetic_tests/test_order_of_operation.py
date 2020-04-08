from basic import Basic
from errors.invalid_syntax_error import InvalidSyntaxError
from errors.unexpected_char_error import UnexpectedCharError
from lang_types.lang_number import LangNumber


def test_parentheses() -> None:
    basic = Basic()

    res, err = basic.run(" let _ = (4 + 2)", "test_single_parentheses")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == (4 + 2)

    res, err = basic.run(" let _ = (4) + 2", "test_single_parentheses")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == (4) + 2

    res, err = basic.run(" let _ = ((4 + 2) + 6)", "test_double_parentheses")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == ((4 + 2) + 6)

    res, err = basic.run(" let _ = -((4 + 2) + 6)", "test_double_parentheses_negation")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == -((4 + 2) + 6)


def test_parentheses_error() -> None:
    basic = Basic()

    res, err = basic.run(" let _ = (4 + 2", "test_unclosed_parentheses_error")
    assert err is not None
    assert res is None
    assert isinstance(err, InvalidSyntaxError)

    res, err = basic.run(" let _ = 4 + 2)", "test_unopened_parentheses_error")
    assert err is not None
    assert res is None
    assert isinstance(err, InvalidSyntaxError)

    res, err = basic.run(" let _ = (4 +) 2", "test_wrong_parentheses_placement")
    assert err is not None
    assert res is None
    assert isinstance(err, InvalidSyntaxError)


def test_order() -> None:
    basic = Basic()

    res, err = basic.run(" let _ = 42 - 6 * 7", "test_order_1")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == 42 - 6 * 7

    res, err = basic.run(" let _ = 7 + 2 * (6 + 3) / 3 - 7", "test_order_2")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == 7 + 2 * (6 + 3) / 3 - 7

    res, err = basic.run(" let _ = 42 - 6 * 7", "test_order_1")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == 42 - 6 * 7

    res, err = basic.run(" let _ = 7 + 2 * (6 + 3) / 3 - 7", "test_order_2")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == 7 + 2 * (6 + 3) / 3 - 7

    res, err = basic.run(" let _ = 42 - 6 * 7", "test_order_1")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == 42 - 6 * 7

    res, err = basic.run(" let _ = 11 + 19 * 2", "test_order_3")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == 11 + 19 * 2

    res, err = basic.run(" let _ = 42 - 6 * 7", "test_order_4")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == 42 - 6 * 7

    res, err = basic.run(" let _ = 7 + 2 * (6 + 3) / 3 - 7", "test_order_5")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == 7 + 2 * (6 + 3) / 3 - 7

    res, err = basic.run(" let _ = (14 + 2) * 2 + 3", "test_order_6")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == (14 + 2) * 2 + 3

    res, err = basic.run(" let _ = 120 / (6 + 12 * 2)", "test_order_7")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == 120 / (6 + 12 * 2)

    res, err = basic.run(" let _ = 12 + 2 * 44", "test_order_8")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == 12 + 2 * 44

    res, err = basic.run(" let _ = 10 * 2 - (7 + 9)", "test_order_9")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == 10 * 2 - (7 + 9)

    res, err = basic.run(" let _ = 2 * 2 ^ 3", "test_order_10")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == 2 * 2 ** 3

    res, err = basic.run(" let _ = 2 * 2 ^ 3 * 2", "test_order_7")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res.value == 2 * 2 ** 3 * 2
