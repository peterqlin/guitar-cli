import click
import readchar
import threading
import time
from rich.live import Live
from .core import Fretboard

running = True
toggle_event = False


def key_listener():
    global running
    global toggle_event
    while running:
        key = readchar.readchar()
        if key == "t":
            toggle_event = True
        if key == "q":
            click.echo("Quitting...")
            running = False


@click.group()
def cli():
    pass


@cli.command()
@click.argument("chord")
@click.option("-v", "--variation", type=int, default=1)
def show(chord, variation):
    global running
    global toggle_event
    listener = threading.Thread(target=key_listener, daemon=True)
    listener.start()

    click.echo("Press t to toggle colors off/on. Press q to quit.")

    f = Fretboard()
    f.set_chord(chord, variation=variation)
    f.show()
    with Live(f.show(), refresh_per_second=4) as live:
        while running:
            if toggle_event:
                toggle_event = False
                f.toggle_rgb_frets()
                live.update(f.show())
            time.sleep(0.05)


@cli.command()
@click.argument("note")
def find(note):
    global running
    listener = threading.Thread(target=key_listener, daemon=True)
    listener.start()

    click.echo(
        "Press any natural note. Press left/down arrow for half step down, right/up arrow for half step up."
    )
