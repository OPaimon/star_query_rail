# type: ignore[attr-defined]
from enum import Enum
from random import choice
from typing import Optional

import typer
from rich.console import Console

from star_query_rail import version
from star_query_rail.example import get_character_info, hello


class Color(str, Enum):
    white = "white"
    red = "red"
    cyan = "cyan"
    magenta = "magenta"
    yellow = "yellow"
    green = "green"


app = typer.Typer(
    name="star_query_rail",
    help="A tool for query some infomation about a game",
    add_completion=False,
)
console = Console()


def version_callback(print_version: bool) -> None:
    """Print the version of the package."""
    if print_version:
        console.print(f"[yellow]star_query_rail[/] version: [bold blue]{version}[/]")
        raise typer.Exit()


@app.command(name="")
def main(
    name: str = typer.Option(..., help="Person to greet."),
    color: Optional[Color] = typer.Option(
        None,
        "-c",
        "--color",
        "--colour",
        case_sensitive=False,
        help="Color for print. If not specified then choice will be random.",
    ),
    print_version: bool = typer.Option(
        None,
        "-v",
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Prints the version of the star_query_rail package.",
    ),
) -> None:
    """Print a greeting with a giving name."""
    if color is None:
        color = choice(list(Color))

    greeting: str = hello(name)
    console.print(f"[bold {color}]{greeting}[/]")


@app.command(name="getCharacterInfo")
def cli_get_character_info(
    cookies: str = typer.Option(..., help="Cookies for query."),
    player_id: int = typer.Option(..., help="Player ID for query."),
    print_version: bool = typer.Option(
        None,
        "-v",
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Prints the version of the star_query_rail package.",
    ),
) -> None:
    """Get character info."""
    get_character_info(cookies, player_id)


if __name__ == "__main__":
    app()
