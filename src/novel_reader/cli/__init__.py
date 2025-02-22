from typer import Typer
from . import translate_cli

app = Typer()
app.add_typer(translate_cli.subcommand)
