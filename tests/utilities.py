from __future__ import annotations

from typing import Optional, TYPE_CHECKING, Any, Type

if TYPE_CHECKING:
    from basic import Basic
    from lang_types.lang_type import LangType
    from errors.error import Error


def run_test(
    basic: Basic,
    code: str,
    name: str,
    res_type: Optional[Type[LangType]] = None,
    err_type: Optional[Type[Error]] = None,
    value: Optional[Any] = None,
) -> None:
    [(res, err)] = basic.run(code, name)
    if res_type:
        assert isinstance(res, res_type)
    else:
        assert res is None
    if err_type:
        assert isinstance(err, err_type)
    else:
        assert err is None

    if value:
        assert res and res.value == value
