from __future__ import annotations

from typing import Optional, TYPE_CHECKING, Any

if TYPE_CHECKING:
    from basic import Basic
    from lang_types.lang_type import LangType
    from errors.error import Error


def run_test(
    basic: Basic,
    code: str,
    name: str,
    res_type: Optional[LangType] = None,
    err_type: Optional[Error] = None,
    value: Optional[Any] = None,
) -> None:
    res, err = basic.run(code, name)
    if res_type:
        assert res is not None
    else:
        assert res is None
    if err_type:
        assert err is not None
    else:
        assert err is None
    if res_type:
        assert isinstance(res, res_type)
    if value:
        assert res.value == value
