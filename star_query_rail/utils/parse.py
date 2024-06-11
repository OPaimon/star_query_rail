from typing import Any, Dict

from arkowrapper import ArkoWrapper


def parse_cookie(text: str) -> Dict[str, Any]:
    """解析 Cookie 字符串"""
    try:
        # cookie str to dict
        wrapped = (
            ArkoWrapper(text.split(";"))
            .filter(lambda x: x != "")
            .map(lambda x: x.strip())
            .map(lambda x: ((y := x.split("=", 1))[0], y[1]))
        )
        cookie = dict(wrapped)
    except (AttributeError, ValueError, IndexError):
        return {}
    return cookie
