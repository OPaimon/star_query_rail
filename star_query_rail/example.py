"""Example of code."""
import asyncio

from star_query_rail.utils.simnet_test import (
    parse_cookie,
    print_character_info_by_query,
)


def hello(name: str) -> str:
    """Just an greetings example.

    Args:
        name (str): Name to greet.

    Returns:
        str: greeting message

    Examples:
        .. code:: python

            >>> hello("Roman")
            'Hello Roman!'
    """
    return f"Hello {name}!"


def get_character_info(cookies: str, player_id: int):
    """Get character info."""
    cookies_parsed = parse_cookie(cookies)
    print("Cookies parsed:", cookies_parsed)
    asyncio.run(print_character_info_by_query(cookies_parsed, player_id))
