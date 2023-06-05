"""Example usage of engorgio with the Person model as a typer cli.

SPDX-FileCopyrightText: 2023-present Waylon S. Walker <waylon@waylonwalker.com>

SPDX-License-Identifier: MIT
"""
import typer

from engorgio import engorgio
from tests.models import Hero, Person

app = typer.Typer(
    name="engorgio",
    help="a demo app",
)


@app.callback()
def main() -> None:
    """Set up typer."""
    return


@app.command()
@engorgio(typer=True)
def get_person(person: Person, thing: str, another: str = "this") -> Person:
    """Get a person's information."""
    from rich import print

    print(thing)
    print(another)

    print(person)
    return person


@app.command()
@engorgio(typer=True)
def get_hero(hero: Hero) -> Hero:
    """Get a hero"""
    from rich import print

    print(hero)


if __name__ == "__main__":
    app()
