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

# globals
running = True
pan_fretboard_toggled = False
pan_key = ""

# `show` globals
rgb_frets_toggled = False
labeled_frets_toggled = False

# `find` globals
note_to_find = ""
find_note_toggled = False


def show_key_listener():
    global running
    global rgb_frets_toggled
    global labeled_frets_toggled
    global pan_fretboard_toggled
    global pan_key
    while running:
        key = readchar.readkey()
        if key == "t":
            rgb_frets_toggled = True
        if key == "y":
            labeled_frets_toggled = True
        if key == readchar.key.LEFT:
            pan_fretboard_toggled = True
            pan_key = "left"
        if key == readchar.key.RIGHT:
            pan_key = "right"
            pan_fretboard_toggled = True
        if key == "q":
            click.echo("Quitting...")
            running = False


def find_key_listener():
    global running
    global note_to_find
    global find_note_toggled
    global pan_fretboard_toggled
    global pan_key
    while running:
        key = readchar.readkey()
        if key in ascii_lowercase[:7]:
            note_to_find = key
            find_note_toggled = True
        if key == readchar.key.UP:
            note_to_find = step(note_to_find, 1)
            find_note_toggled = True
        if key == readchar.key.DOWN:
            note_to_find = step(note_to_find, -1)
            find_note_toggled = True
        if key == readchar.key.LEFT:
            pan_fretboard_toggled = True
            pan_key = "left"
        if key == readchar.key.RIGHT:
            pan_key = "right"
            pan_fretboard_toggled = True
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
    global rgb_frets_toggled
    global labeled_frets_toggled
    global pan_fretboard_toggled
    global pan_key
    listener = threading.Thread(target=show_key_listener, daemon=True)
    listener.start()

    click.echo(
        "Press t to toggle colors off/on. Press y to toggle labeled frets. Press q to quit."
    )

    f = Fretboard("chord")
    f.set_chord(chord, variation=variation)
    f.render()
    with Live(f.render(), refresh_per_second=4) as live:
        while running:
            if rgb_frets_toggled:
                rgb_frets_toggled = False
                f.toggle_rgb_frets()
            if labeled_frets_toggled:
                labeled_frets_toggled = False
                f.toggle_labeled_frets()
            if pan_fretboard_toggled:
                pan_fretboard_toggled = False
                f.pan_fretboard(1 if pan_key == "right" else -1)

            live.update(f.render())
            time.sleep(0.05)


@cli.command()
@click.argument("note")
def find(note):
    global running
    global note_to_find
    global find_note_toggled
    global pan_fretboard_toggled
    global pan_key
    listener = threading.Thread(target=find_key_listener, daemon=True)
    listener.start()

    click.echo(
        "Press any natural note or move a half step up or down with the arrow keys."
    )

    note_to_find = note
    f = Fretboard("find")
    f.set_find_note(note_to_find)
    f.render()
    with Live(f.render(), refresh_per_second=4) as live:
        while running:
            if find_note_toggled:
                find_note_toggled = False
                f.set_find_note(note_to_find)
            if pan_fretboard_toggled:
                pan_fretboard_toggled = False
                f.pan_fretboard(1 if pan_key == "right" else -1)

            live.update(f.render())
            f.render()
            time.sleep(0.05)
