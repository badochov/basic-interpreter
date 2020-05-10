from basic import Basic
from errors.invalid_syntax_error import InvalidSyntaxError
from lang_types.lang_number import LangNumber


def test_wrong_syntax_assignment() -> None:
    return
    basic = Basic()

    res, err = basic.run("a let 0 =", "test_wrong_order_assignment")
    assert err is not None
    assert res is None
    assert isinstance(err, InvalidSyntaxError)

    res, err = basic.run("a let = 0", "test_wrong_order_assignment_2")
    assert err is not None
    assert res is None
    assert isinstance(err, InvalidSyntaxError)

    res, err = basic.run("0 = let a", "test_wrong_order_assignment_3")
    assert err is not None
    assert res is None
    assert isinstance(err, InvalidSyntaxError)

    res, err = basic.run("= 0 let a", "test_wrong_order_assignment_4")
    assert err is not None
    assert res is None
    assert isinstance(err, InvalidSyntaxError)

    res, err = basic.run("1 + let a = 0", "test_wrong_order_assignment_5")
    assert err is not None
    assert res is None
    assert isinstance(err, InvalidSyntaxError)


def test_integer_assignment() -> None:
    basic = Basic()

    res, err = basic.run("let a1 = 0", "test_positive_integer_assignment")
    print(res, err)
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res._value == 0

    res, err = basic.run("let a2 = -2", "test_negative_integer_assignment")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res._value == -2

    res, err = basic.run("let a3 = 2 + 2", "test_addition_integer_assignment_part1")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res._value == 4
    res, err = basic.run("let _ = a3", "test_addition_integer_assignment_part2")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res._value == 4

    res, err = basic.run(
        "let a4 = 2 + 2", "test_multiplication_integer_assignment_part1"
    )
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res._value == 4
    res, err = basic.run("let _ = a4", "test_multiplication_integer_assignment_part2")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res._value == 4

    res, err = basic.run(
        "let a5 = 2 ^ 2", "test_raised_to_power_integer_assignment_part1"
    )
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res._value == 4
    res, err = basic.run("let _ = a5", "test_raised_to_power_integer_assignment_part2")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res._value == 4

    res, err = basic.run(
        "let a6 = (let a7 = 2 in a7) * (let a8 = 1 in a8) * (let a9 = 3 in a9) * (let a10 = 7 in a10)",
        "test_assignement_output_part1",
    )
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res._value == 2 * 1 * 3 * 7
    res, err = basic.run("let _ = a6", "test_assignement_output_part2")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res._value == 2 * 1 * 3 * 7
    res, err = basic.run("let _ = a7", "test_assignement_output_part3")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res._value == 2
    res, err = basic.run("let _ = a8", "test_assignement_output_part4")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res._value == 1
    res, err = basic.run("let _ = a9", "test_assignement_output_part5")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res._value == 3
    res, err = basic.run("let _ = a10", "test_assignement_output_part6")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res._value == 7

    res, err = basic.run(
        "let a11 = (let a12 = 2 in a12)", "test_multi_assignement_part1",
    )
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res._value == 2
    res, err = basic.run("let _ = a11", "test_multi_assignement_part2")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res._value == 2
    res, err = basic.run("let _ = a12", "test_multi_assignement_part3")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res._value == 2


def test_float_assignment() -> None:
    basic = Basic()

    res, err = basic.run("let a1 = 0.7", "test_positive_float_assignment")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res._value == 0.7

    res, err = basic.run("let a2 = -0.7", "test_negative_float_assignment")
    assert err is None
    assert res is not None
    assert isinstance(res, LangNumber)
    assert res._value == -0.7
