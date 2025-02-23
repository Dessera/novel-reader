from typing import Annotated, Optional
from typer import Typer, Option
from tqdm import tqdm

from ..utils.factories import TranslatorFactory, FetcherFactory

subcommand = Typer(name="translate", help="Translate novels")


@subcommand.command(help="Translate a single page")
def single(
    source_type: Annotated[str, Option(help="The source type of the novel")],
    translator_type: Annotated[str, Option(help="The type of translator to use")],
    source: Annotated[str, Option(help="The source url of the novel")],
    output: Annotated[
        Optional[str],
        Option(help="The output file path, if not specified, will print to stdout"),
    ] = None,
    source_params: Annotated[str, Option(help="The parameters for the source")] = "{}",
    translator_params: Annotated[
        str, Option(help="The parameters for the translator")
    ] = "{}",
):
    try:
        fetcher_factory = FetcherFactory()
        fetcher = fetcher_factory.create(source_type, source_params)

        translator_factory = TranslatorFactory()
        translator = translator_factory.create(translator_type, translator_params)

        doc = fetcher.fetch(source)

        if output:
            with open(output, "w", encoding="utf-8") as f:
                for sec in tqdm(doc.sections, unit="section"):
                    f.write(f"{translator.translate(sec)}\n")
        else:
            result = ""
            for sec in tqdm(doc.sections, unit="section"):
                result += f"{translator.translate(sec)}\n"
            print(result)
    except Exception as e:
        print(e)
