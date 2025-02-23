from typing import Annotated
from typer import Option, Typer

from . import help_cli, translate_cli

from ..exceptions import BaseReaderException
from ..utils.factories import FetcherFactory

app = Typer()

app.add_typer(translate_cli.subcommand)
app.add_typer(help_cli.subcommand)


@app.command(help="Fetch novels to json")
def fetch(
    src: Annotated[str, Option(help="Novel source")],
    dst: Annotated[str, Option(help="Json file to save")],
    fetcher: Annotated[str, Option(help="Fetcher name")],
    all: Annotated[
        bool, Option(help="Fetch all chapters, need corresponding src")
    ] = False,
    params: Annotated[str, Option(help="Fetcher params")] = "{}",
):
    try:
        factory = FetcherFactory()
        fetcher_obj = factory.create(fetcher, params)
        if all:
            res = fetcher_obj.fetch_all(src).to_json()
        else:
            res = fetcher_obj.fetch(src).to_json()

        with open(dst, "w") as f:
            f.write(res)
    except BaseReaderException as e:
        print(e)
    except Exception as e:
        print(f"Unhandled exception occurred: \n{e}")
