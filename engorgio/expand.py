"""
Exapand model function arguments to fields.

Core implementation of engorgio to expand pydantic arguments.

SPDX-FileCopyrightText: 2023-present Waylon S. Walker <waylon@waylonwalker.com>

SPDX-License-Identifier: MIT
"""

import inspect
import os
from typing import Callable, Dict, Optional

import black
from pydantic.fields import ModelField


def create_default(field: ModelField) -> str:
    """Create the default value for pydantic ModelFields."""
    if "=" not in repr(field) and not hasattr(field, "required"):
        default = ""
    if "=" not in repr(field) and hasattr(field, "required"):
        default = ""
    elif not hasattr(field, "required"):
        default = f'="{field.default}"'
    elif field.default is None and not getattr(field, "required", False):
        default = "=None"
    elif field.default is not None:
        default = f'="{field.default}"'
    else:
        default = ""

    return default


def create_default_typer(
    panel_name: str,
    field: ModelField,
    *,
    prompt_always: bool = False,
) -> str:
    """Create the default value for pydantic ModelFields for typer functions."""
    prompt = ""
    if prompt_always:
        prompt = ", prompt=True"
    if "=" not in repr(field) and not hasattr(field, "required"):
        default = ""
    if "=" not in repr(field) and hasattr(field, "required"):
        default = "=None"
    elif not hasattr(field, "required"):
        default = f'="{field.default}"'
    elif field.default is None and not getattr(field, "required", False):
        default = f' = typer.Option(None, help="{field.field_info.description or ""}", rich_help_panel="{panel_name}"{prompt})'
    elif field.default is not None:
        default = f' = typer.Option("{field.default}", help="{field.field_info.description or ""}", rich_help_panel="{panel_name}"{prompt})'
    else:
        default = f' = typer.Option(..., help="{field.field_info.description or ""}", rich_help_panel="{panel_name}", prompt=True)'
    return default


def make_annotation(
    name: str,
    field: ModelField,
    # parents: Dict[str, str],
    model_separator: str = "__",
    *,
    typer: bool = False,
    prompt_always: bool = False,
) -> str:
    """Create an annotation for pydantic ModelFields."""
    # might still need this when parents=False
    # while next_name is not None:
    #     if next_name is not None:

    annotation = (
        field.annotation.__name__
        if str(field.annotation).startswith("<")
        else str(field.annotation)
    )
    annotation = f": {annotation}" if annotation != "_empty" else ""
    if typer:
        default = create_default_typer(
            panel_name="--".join(name.split(model_separator)[:-1]),
            field=field,
            prompt_always=prompt_always,
        )
    else:
        default = create_default(
            field=field,
        )

    return f"{name}{annotation}{default}"


def init_more_args(
    func: Callable,
    more_args: Dict,
    model_separator: str = "__",
    *,
    include_parent_model: bool = False,
) -> Dict:
    """Initialize the more_args dict."""
    parents = {}
    sig = inspect.signature(func)
    for name, param in sig.parameters.items():
        if hasattr(param.annotation, "__fields__"):
            if include_parent_model:
                new_param = {
                    f"{name}{model_separator}{k}": v
                    for k, v in param.annotation.__fields__.items()
                }
            else:
                new_param = param.annotation.__fields__
            more_args = {**more_args, **new_param}
            for field in param.annotation.__fields__:
                parents[field] = param.annotation.__name__
        else:
            more_args[name] = param
        return more_args, parents
    return None


def get_more_args(
    func: Callable,
    model_separator: str = "__",
    *,
    include_parent_model: Optional[bool] = None,
    more_args: Optional[Dict] = None,
) -> Dict:
    """Get the more_args dict."""
    if more_args is None:
        more_args = {}
    more_args, parents = init_more_args(
        func=func,
        model_separator=model_separator,
        include_parent_model=include_parent_model,
        more_args=more_args,
    )

    while any(
        hasattr(param.annotation, "__fields__") for name, param in more_args.items()
    ):
        keys_to_remove = []
        for name, param in more_args.items():
            if hasattr(param.annotation, "__fields__"):
                # model parent lookup

                if name not in param.annotation.__fields__.keys():
                    keys_to_remove.append(name)

                if include_parent_model:
                    new_param = {
                        f"{name}{model_separator}{k}": v
                        for k, v in param.annotation.__fields__.items()
                    }
                else:
                    new_param = param.annotation.__fields__

                more_args = {**more_args, **new_param}

                for field in param.annotation.__fields__:
                    parents[field] = param.annotation.__name__

        for key in keys_to_remove:
            del more_args[key]
    return more_args


def make_expanded_function(
    func: Callable,
    wrapper: Callable,
    model_separator: str = "__",
    *,
    include_parent_model: bool = True,
    typer: bool = False,
):
    """Return a new function with that accepts model fields."""
    more_args = get_more_args(
        func=func,
        model_separator=model_separator,
        include_parent_model=include_parent_model,
    )

    annotations = [
        make_annotation(
            name=name,
            field=field,
            model_separator=model_separator,
            typer=typer,
        )
        for name, field in more_args.items()
    ]

    # split raw_args into args and kwargs
    aargs = ", ".join([arg for arg in annotations if "=" not in arg])
    kwargs = ", ".join([arg for arg in annotations if "=" in arg])

    # args to call the wrapper function with
    call_args = ",".join([f"{name}={name}" for name in more_args])

    # update the docscring
    wrapper.__doc__ = (
        func.__doc__ or ""
    ) + f"\nalso accepts {more_args.keys()} in place of person model"

    new_func_str = f"""
import typer
def {func.__name__}({aargs}{', ' if aargs else ''}{kwargs}):
    '''{func.__doc__}'''
    return wrapper({call_args})
    """
    new_func_str = black.format_str(src_contents=new_func_str, mode=black.FileMode())

    pyflyby_log_level = os.getenv("PYFLYBY_LOG_LEVEL")
    if pyflyby_log_level is None:
        os.environ["PYFLYBY_LOG_LEVEL"] = "WARNING"

    import pyflyby

    pyflyby.auto_import(new_func_str, locals())

    exec(new_func_str, locals(), globals())  # noqa: S102
    new_func = globals()[func.__name__]

    sig = inspect.signature(new_func)
    for param in sig.parameters.values():
        if hasattr(param.annotation, "__fields__"):
            return make_expanded_function(
                new_func,
                wrapper,
                typer=typer,
                model_separator=model_separator,
            )
    return new_func
