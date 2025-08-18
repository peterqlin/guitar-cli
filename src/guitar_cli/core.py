import sys
import time
from rich.console import Console
from .utils import get_fret_spacing


class Fretboard:
    def __init__(self, fretboard_length=200, fret_count=12, rgb_frets=True) -> None:
        self.console = Console()  # create console for rich printing
        self.rgb_frets = rgb_frets  # toggle colored frets
        self.fret_spacing = get_fret_spacing(fretboard_length, fret_count)
        self.color_map = {
            "e": (31, 119, 180),  # Blue
            "f": (255, 127, 14),  # Orange
            "f#": (44, 160, 44),  # Green
            "g": (214, 39, 40),  # Red
            "g#": (148, 103, 189),  # Purple
            "a": (140, 86, 75),  # Brown
            "a#": (227, 119, 194),  # Pink
            "b": (127, 127, 127),  # Gray
            "c": (188, 189, 34),  # Olive
            "c#": (23, 190, 207),  # Teal
            "d": (255, 152, 150),  # Light Red
            "d#": (197, 176, 213),  # Lavender
        }

        self.chord = [0] * 6  # initialize chord array

        # TODO: allow toggle between equivalent sharps and flats
        self.chromatic_scale = [
            "c",
            "c#",
            "d",
            "d#",
            "e",
            "f",
            "f#",
            "g",
            "g#",
            "a",
            "a#",
            "b",
        ]  # initialize chromatic scale

        # TODO: maybe change how this is stored, but for now it'll work
        init_pos = [
            self.chromatic_scale.index(n) for n in ["e", "b", "g", "d", "a", "e"]
        ]  # get initial note positions, high e to low e
        # TODO: change this to adapt to > 12 frets
        self.fretboard = [
            self.chromatic_scale[pos:] + self.chromatic_scale[:pos] for pos in init_pos
        ]  # create fretboard with inc indices corresponding to lower pitch strings

        try:
            with open(
                "src/guitar_cli/headstock_ascii_art.txt", "r", encoding="utf-8"
            ) as f:
                self.headstock = [
                    "[rgb(240,240,240)]" + line.rstrip("\n") + "[/]" for line in f
                ]  # use white; some special characters are colored by default
        except Exception as e:
            print(f"Failed to load headstock ASCII art: {e}")
            self.headstock = []

    def show(self) -> None:
        """
        Handle rendering the fretboard
        """
        try:
            self.console.clear()  # clear stdout
            strung_fretboard = []
            for string_idx, notes in enumerate(self.fretboard):
                strung_notes = []
                for note_idx, note in enumerate(notes):
                    strung_note = f"{note:{'-' if string_idx < 3 else '='}<{self.fret_spacing[note_idx]}}"
                    dash_string = strung_note[
                        len(note) :
                    ]  # extract the string of hyphens
                    if self.rgb_frets:
                        r, g, b = self.color_map[note]
                        styled_note = (
                            f"[rgb({r},{g},{b})]{note}[/]"  # use color from color map
                        )
                        r2, g2, b2 = self.color_map[
                            self.chromatic_scale[
                                (self.chromatic_scale.index(note) + 1)
                                % len(self.chromatic_scale)
                            ]
                        ]
                        styled_dash_string = f"[rgb({r2},{g2},{b2})]{dash_string}[/]"  # use color from color map
                        strung_note = f"{styled_note}{styled_dash_string}"
                    else:
                        strung_note = f"[rgb(240,240,240)]{note}{dash_string}[/]"  # use white; equal sign has it's own coloring rules
                    strung_notes.append(strung_note)
                strung_fretboard.append(strung_notes)
            headstock_copy = self.headstock.copy()
            # TODO: make this not so hard-coded
            headstock_copy[3] += "".join(
                ["_"] * sum(self.fret_spacing)
            )  # extend the neck of the guitar as necessary
            for i, string in zip(range(4, 10), strung_fretboard):
                headstock_copy[i] += "".join(string)
            rendered_fretboard = "\n".join(headstock_copy)

            # self.console.log(rendered_fretboard, markup=False)
            self.console.print(rendered_fretboard)
            time.sleep(2)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def set_chord(self, chord: list[int]) -> None:
        try:
            self.chord = chord
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
