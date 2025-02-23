from typing import Annotated, Dict, Type
from pydantic.fields import FieldInfo
from typer import Typer, Argument

from ..utils.params_object import ParamsObjectFactory, ParamsObject
from ..utils.factories import TranslatorFactory, FetcherFactory

subcommand = Typer(name="help", help="Detail help for modules")


@subcommand.command()
def fetcher(
    name: Annotated[str, Argument(help="Fetcher name")],
):
    inspect_module(FetcherFactory(), name)


@subcommand.command()
def translator(
    name: Annotated[str, Argument(help="Translator name")],
):
    inspect_module(TranslatorFactory(), name)


def inspect_module[T: ParamsObject](factory: ParamsObjectFactory[T], identifier: str):
    obj = factory.get_object(identifier)
    if obj is None:
        print(f"No module named {identifier} found")
        return
    print_meta(obj)
    print_fields(obj.Config.model_fields)


def print_meta(obj: Type[ParamsObject]):
    print("module:")
    print(f"    name: {obj.Meta.identifier}")


def print_fields(fields: Dict[str, FieldInfo]):
    print("params:")
    for k, v in fields.items():
        print(f"    {k}:")
        print(f"        type: {v.annotation}")
        print(f"        default: {v.default}")
        print(f"        description: {v.description}")
