---
title: Tutorial
---

Parent model names are now in the argument names. Here are some
examples using a Hero who has a Pet, and both have a name.
Previously name would have collided between them.

```python
class Pet(BaseModel):
    name: str = Field(..., description="The pet's name.")


class Hero(BaseModel):
    name: str = Field(..., description="The hero's name.")
    pet: Pet = Field(..., description="The hero's pet.")


@engorgio()
def get_hero(hero: Hero) -> Hero:
    """Mydocstring."""
    return hero

help(get_hero)
```

> creating a get_hero function

```python
Help on function get_hero:

get_hero(hero__name: str, hero__pet__name: str)
    Mydocstring.
```

> output

```python
from typer import Typer

app = Typer()

@app.command()
@engorgio(typer=True)
def get_hero(hero: Hero) -> Hero:
    """Get a hero"""
    from rich import print

    print(hero)

if __name__ == "__main__":
    typer.run(get_hero)

```

> example using typer

```console
❯ hatch run python examples/person_cli.py get-hero --help

 Usage: person_cli.py get-hero [OPTIONS]

 Get a hero

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ hero ───────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --hero--name        TEXT  The hero's name. [default: None] [required]                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ hero--pet ──────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --hero--pet--name        TEXT  The pet's name. [default: None] [required]                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```

> help output
