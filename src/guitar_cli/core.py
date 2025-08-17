from rich.console import Console
from .utils import get_fret_spacing


class Fretboard:
    def __init__(
        self, fretboard_length=300, fret_count=12, rgb_frets=True, twelve_string=False
    ) -> None:
        self.console = Console()  # create console for rich printing
        self.rgb_frets = rgb_frets  # toggle colored frets
        self.fret_spacing = get_fret_spacing(fretboard_length, fret_count)
        self.fill_char = "=" if twelve_string else "-"
        # TODO: make the color difference between sharp and natural notes more obvious
        self.color_map = {
            "e": (228, 3, 3),  # Red
            "f": (255, 140, 0),  # Orange
            "f#": (255, 165, 0),
            "g": (255, 237, 0),  # Yellow
            "g#": (255, 252, 0),
            "a": (0, 128, 38),  # Green
            "a#": (0, 143, 53),
            "b": (0, 77, 255),  # Blue
            "c": (75, 0, 130),  # Indigo
            "c#": (90, 0, 145),
            "d": (117, 7, 135),  # Violet
            "d#": (132, 7, 150),
        }
        self.chord = [0] * 6  # initialize chord array

        chromatic_scale = [
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
            chromatic_scale.index(n) for n in ["e", "b", "g", "d", "a", "e"]
        ]  # get initial note positions, high e to low e
        # TODO: change this to adapt to > 12 frets
        self.fretboard = [
            chromatic_scale[pos:] + chromatic_scale[:pos] for pos in init_pos
        ]  # create fretboard with inc indices corresponding to lower pitch strings

    def show(self) -> None:
        """
        Handle rendering the fretboard
        """
        try:
            strung_fretboard = []
            for notes in self.fretboard:
                strung_notes = []
                for i, note in enumerate(notes):
                    strung_note = ""
                    if i == 0:
                        strung_note = note  # don't give open notes a left dash
                    else:
                        strung_note = f"{note:{self.fill_char}>{self.fret_spacing[i]}}"  # dash to left of fret representing note region
                    if self.rgb_frets:
                        r, g, b = self.color_map[note]
                        strung_note = f"[rgb({r},{g},{b})]{strung_note}[/]"  # use color from color map
                    else:
                        strung_note = f"[rgb(240,240,240)]{strung_note}[/]"  # use white; equal sign has it's own coloring rules
                    strung_notes.append(strung_note)
                strung_fretboard.append(strung_notes)
            rendered_fretboard = "\n".join(
                ["".join(string) for string in strung_fretboard]
            )

            # self.console.log(rendered_fretboard, markup=False)
            self.console.print(rendered_fretboard)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def set_chord(self, chord: list[int]) -> None:
        try:
            self.chord = chord
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
