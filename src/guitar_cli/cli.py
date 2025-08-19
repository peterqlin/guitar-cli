import click
import readchar
import threading
import time
from string import ascii_lowercase
from rich.live import Live
from .core import Fretboard

running = True

# `show` globals
rgb_frets_toggled = False
labeled_frets_toggled = False

# `find` globals
note_to_find = "e"
note_toggled = False


def show_key_listener():
    global running
    global rgb_frets_toggled
    global labeled_frets_toggled
    while running:
        key = readchar.readchar()
        if key == "t":
            rgb_frets_toggled = True
        if key == "y":
            labeled_frets_toggled = True
        if key == "q":
            click.echo("Quitting...")
            running = False


def find_key_listener():
    global running
    global note_to_find
    global note_toggled
    while running:
        key = readchar.readchar()
        if key in ascii_lowercase[:7]:
            note_to_find = key
            note_toggled = True
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

            live.update(f.render())
            time.sleep(0.05)


@cli.command()
@click.argument("note")
def find(note):
    global running
    global note_to_find
    global note_toggled
    listener = threading.Thread(target=find_key_listener, daemon=True)
    listener.start()

    click.echo(
        "Press any natural note. Press left/down arrow for half step down, right/up arrow for half step up."
    )

    f = Fretboard("find")
    f.set_find_note(note)
    f.render()
    with Live(f.render(), refresh_per_second=4) as live:
        while running:
            if note_toggled:
                note_toggled = False
                f.set_find_note(note_to_find)

            live.update(f.render())
            time.sleep(0.05)
