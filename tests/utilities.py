from __future__ import annotations

from typing import Optional, TYPE_CHECKING, Any, Type, List, Union

from errors.error import Error
from errors.invalid_syntax_error import InvalidSyntaxError
from errors.rt_error import RTError

if TYPE_CHECKING:
    from basic import Basic
    from lang_types.lang_type import LangType

    type_res = Optional[Union[List[Type[LangType]], Type[LangType]]]
    type_err = Optional[Type[Error]]
    type_value = Optional[Union[List[Union[Any]], Any]]


def run_test(
    basic: Basic,
    code: str,
    name: str,
    res_type: type_res = None,
    err_type: type_err = None,
    value: type_value = None,
    repl: bool = True,
) -> None:
    if not isinstance(res_type, list):
        res_type = [res_type] if res_type else []
    if not isinstance(value, list):
        value = [value] if value is not None else []
    try:
        results = basic.run(code, name, repl)
        assert len(results) == len(res_type)
        for i, res in enumerate(results):
            assert res_type and isinstance(res, res_type[i])
            if value and value[i] is not Ellipsis:
                if res.value != value[i]:
                    print(res.value, value[i])
                assert res.value == value[i]
    except Error as err:
        assert err_type and isinstance(err, err_type)
    else:
        assert err_type is None


def run_test_correct(
    basic: Basic, code: str, name: str, res_type: type_res, value: type_value = None,
) -> None:
    run_test(basic, code, name, res_type, None, value)


def run_test_error(basic: Basic, code: str, name: str, err_type: type_err) -> None:
    run_test(basic, code, name, None, err_type)


def run_test_rt_error(basic: Basic, code: str, name: str) -> None:
    run_test(basic, code, name, None, RTError)


def run_test_invalid_syntax_error(basic: Basic, code: str, name: str) -> None:
    run_test(basic, code, name, None, InvalidSyntaxError)
