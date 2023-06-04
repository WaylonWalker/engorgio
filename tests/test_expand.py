from engorgio.expand import make_annotation

from . import models


def test_make_annotation_person_name():
    assert (
        make_annotation("name", models.Person.__fields__["name"], {"name": "person"}) ==
        "name: str"
    )


def test_make_annotation_person_name_typer():
    assert (
        make_annotation(
            "name",
            models.Person.__fields__["name"],
            {"name": "person"},
            typer=True,
        ) ==
        'name: str = typer.Option(..., help="The name of the person.", rich_help_panel="person", prompt=True)'
    )


def test_make_annotation_person_alias():
    assert (
        make_annotation("name", models.Person.__fields__["alias"], {"name": "person"}) ==
        "name: typing.Optional[str]=None"
    )


def test_make_annotation_person_alias_typer():
    assert (
        make_annotation(
            "name",
            models.Person.__fields__["alias"],
            {"name": "person"},
            typer=True,
        ) ==
        'name: typing.Optional[str] = typer.Option(None, help="An optional other name for the person.", rich_help_panel="person")'
    )


def test_make_annotation_person_alias_typer_prompt_always():
    assert (
        make_annotation(
            "name",
            models.Person.__fields__["alias"],
            {"name": "person"},
            typer=True,
            prompt_always=True,
        ) ==
        'name: typing.Optional[str] = typer.Option(None, help="An optional other name for the person.", rich_help_panel="person", prompt=True)'
    )


def test_make_annotation_person_age():
    assert (
        make_annotation("age", models.Person.__fields__["age"], {"age": "person"}) ==
        "age: int"
    )


def test_make_annotation_person_email():
    assert (
        make_annotation("email", models.Person.__fields__["email"], {"email": "person"}) ==
        "email: typing.Optional[str]=None"
    )


def test_make_annotation_person_pet():
    assert (
        make_annotation("pet", models.Person.__fields__["pet"], {"pet": "person"}) ==
        'pet: str="dog"'
    )


def test_make_annotation_alpha_a():
    assert (
        make_annotation("a", models.Alpha.__fields__["a"], {"a": "alpha"}) == "a: int"
    )


def test_make_annotation_color_alpha():
    assert (
        make_annotation(
            "alpha", models.Color.__fields__["alpha"], {"a": "alpha", "alpha": "color"}
        ) ==
        "alpha: Alpha"
    )
