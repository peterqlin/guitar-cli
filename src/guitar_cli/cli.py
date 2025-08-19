import click
import readchar
import threading
import time
from string import ascii_lowercase
from rich.live import Live
from .core import Fretboard
from .utils import step
from rich.traceback import install

install()

state = {
    "running": True,
    "pan_fretboard_toggled": False,
    "pan_key": "",
    "rgb_frets_toggled": False,
    "labeled_frets_toggled": False,
    "note_to_find": "",
    "find_note_toggled": False,
    "pan_distance": 3,
}


def show_key_listener():
    while state["running"]:
        key = readchar.readkey()
        if key == "t":
            state["rgb_frets_toggled"] = True
        if key == "y":
            state["labeled_frets_toggled"] = True
        if key == readchar.key.LEFT:
            state["pan_fretboard_toggled"] = True
            state["pan_key"] = "left"
        if key == readchar.key.RIGHT:
            state["pan_key"] = "right"
            state["pan_fretboard_toggled"] = True
        if key == "q":
            click.echo("Quitting...")
            state["running"] = False


def find_key_listener():
    while state["running"]:
        key = readchar.readkey()
        if key in ascii_lowercase[:7]:
            state["note_to_find"] = key
            state["find_note_toggled"] = True
        if key == readchar.key.UP:
            state["note_to_find"] = step(state["note_to_find"], 1)
            state["find_note_toggled"] = True
        if key == readchar.key.DOWN:
            state["note_to_find"] = step(state["note_to_find"], -1)
            state["find_note_toggled"] = True
        if key == readchar.key.LEFT:
            state["pan_fretboard_toggled"] = True
            state["pan_key"] = "left"
        if key == readchar.key.RIGHT:
            state["pan_key"] = "right"
            state["pan_fretboard_toggled"] = True
        if key == "q":
            click.echo("Quitting...")
            state["running"] = False


@click.group()
def cli():
    pass


@cli.command()
@click.argument("chord")
@click.option("-v", "--variation", type=int, default=1)
def show(chord, variation):
    listener = threading.Thread(target=show_key_listener, daemon=True)
    listener.start()

    click.echo(
        "Press t to toggle colors off/on. Press y to toggle labeled frets. Press left/right arrow to pan. Press q to quit."
    )

    f = Fretboard("chord")
    f.set_chord(chord, variation=variation)
    f.render()
    with Live(f.render(), refresh_per_second=4) as live:
        while state["running"]:
            if state["rgb_frets_toggled"]:
                state["rgb_frets_toggled"] = False
                f.toggle_rgb_frets()
            if state["labeled_frets_toggled"]:
                state["labeled_frets_toggled"] = False
                f.toggle_labeled_frets()
            if state["pan_fretboard_toggled"]:
                state["pan_fretboard_toggled"] = False
                f.pan_fretboard(state["pan_key"], state["pan_distance"])

            live.update(f.render())
            time.sleep(0.05)


@cli.command()
@click.argument("note")
def find(note):
    listener = threading.Thread(target=find_key_listener, daemon=True)
    listener.start()

    click.echo(
        "Press any natural note or move a half step up or down with the arrow keys. Press left/right arrow to pan."
    )

    state["note_to_find"] = note
    f = Fretboard("find")
    f.set_find_note(state["note_to_find"])
    f.render()
    with Live(f.render(), refresh_per_second=4) as live:
        while state["running"]:
            if state["find_note_toggled"]:
                state["find_note_toggled"] = False
                f.set_find_note(state["note_to_find"])
            if state["pan_fretboard_toggled"]:
                state["pan_fretboard_toggled"] = False
                f.pan_fretboard(state["pan_key"], state["pan_distance"])

            live.update(f.render())
            f.render()
            time.sleep(0.05)
