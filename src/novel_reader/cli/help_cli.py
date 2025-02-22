from typing import Annotated, Dict
from pydantic.fields import FieldInfo
from typer import Typer, Argument

from ..translators import TranslatorFactory
from ..fetchers import FetcherFactory

subcommand = Typer(name="module-help", help="Detail help for modules")


@subcommand.command()
def fetcher(
    name: Annotated[str, Argument(help="Fetcher name")],
):
    fetcher_factory = FetcherFactory()
    fetcher = fetcher_factory.fetchers.get(name)
    if fetcher is None:
        print(f"No fetcher named {name} found")
        return
    print_fields(fetcher.Config.model_fields)


@subcommand.command()
def translator(
    name: Annotated[str, Argument(help="Translator name")],
):
    translator_factory = TranslatorFactory()
    translator = translator_factory.translators.get(name)
    if translator is None:
        print(f"No translator named {name} found")
        return
    print_fields(translator.Config.model_fields)


def print_fields(fields: Dict[str, FieldInfo]):
    for k, v in fields.items():
        print(f"{k}:")
        print(f"    type: {v.annotation}")
        print(f"    default: {v.default}")
        print(f"    description: {v.description}")
