from __future__ import annotations

from typing import Optional, TYPE_CHECKING, Any, Type

from errors.error import Error

if TYPE_CHECKING:
    from basic import Basic
    from lang_types.lang_type import LangType


def run_test(
    basic: Basic,
    code: str,
    name: str,
    res_type: Optional[Type[LangType]] = None,
    err_type: Optional[Type[Error]] = None,
    value: Optional[Any] = None,
) -> None:
    try:
        [res] = basic.run(code, name, True)
        assert res_type and isinstance(res, res_type)
        if value:
            assert res and res.value == value
    except Error as err:
        assert err_type and isinstance(err, err_type)
