import click
from .core import Fretboard


@click.group()
def cli():
    pass


@cli.command()
def show():
    f = Fretboard()
    f.show()
