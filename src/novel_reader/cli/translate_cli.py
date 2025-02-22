from typing import Annotated
from typer import Typer, Option

from ..translators import TranslatorFactory
from ..fetchers import FetcherFactory

subcommand = Typer(name="translate", help="Translate novels")


@subcommand.command(help="Translate a single page")
def single(
    source_type: Annotated[str, Option(help="The source type of the novel")],
    source: Annotated[str, Option(help="The source url of the novel")],
    translator_type: Annotated[str, Option(help="The type of translator to use")],
    source_params: Annotated[str, Option(help="The parameters for the source")] = "{}",
    translator_params: Annotated[
        str, Option(help="The parameters for the translator")
    ] = "{}",
):
    try:
        fetcher_factory = FetcherFactory()
        fetcher = fetcher_factory.create_fetcher(source_type, source_params)

        translator_factory = TranslatorFactory()
        translator = translator_factory.create_translator(
            translator_type, translator_params
        )

        print(fetcher)
        print(fetcher.params)
        print(fetcher.params_info)

        print(translator)
        print(translator.params)
        print(translator.params_info)
    except Exception as e:
        print(e)
