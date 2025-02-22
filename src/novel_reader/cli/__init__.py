from typer import Typer
from . import help_cli, translate_cli

app = Typer()

app.add_typer(translate_cli.subcommand)
app.add_typer(help_cli.subcommand)
