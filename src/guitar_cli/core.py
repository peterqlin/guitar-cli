from rich.console import Console
from .utils import get_fret_spacing, get_rgb_text


class Fretboard:
    def __init__(self, fretboard_length=200, fret_count=12, rgb_frets=True) -> None:
        self.console = Console()
        self.rgb_frets = rgb_frets
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

        self.chord = [0] * 6

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
        ]

        self.chord_names = [
            "A",
            "Am",
            "A7",
            "Amaj7",
            "B",
            "Bm",
            "B7",
            "Bmaj7",
            "C",
            "Cm",
            "C7",
            "Cmaj7",
            "D",
            "Dm",
            "D7",
            "Dmaj7",
            "E",
            "Em",
            "E7",
            "Emaj7",
            "F",
            "Fm",
            "F7",
            "Fmaj7",
            "G",
            "Gm",
            "G7",
            "Gmaj7",
        ]

        # TODO: maybe change how this is stored, but for now it'll work
        # get initial note positions, high e to low e
        init_pos = [
            self.chromatic_scale.index(n) for n in ["e", "b", "g", "d", "a", "e"]
        ]
        # TODO: change this to adapt to > 12 frets
        # create fretboard with inc indices corresponding to lower pitch strings
        self.fretboard = [
            self.chromatic_scale[pos:] + self.chromatic_scale[:pos] for pos in init_pos
        ]

        try:
            with open(
                "src/guitar_cli/headstock_ascii_art.txt", "r", encoding="utf-8"
            ) as f:
                # set color of ascii art to white
                self.headstock = [get_rgb_text(line.rstrip("\n")) for line in f]
        except Exception as e:
            self.console.log(f"Failed to load headstock ASCII art: {e}")
            self.headstock = []

    def toggle_rgb_frets(self) -> None:
        self.rgb_frets = not self.rgb_frets

    def show(self) -> None:
        """
        Handle rendering the fretboard
        """
        try:
            self.console.clear()
            strung_fretboard = []
            for string_idx, notes in enumerate(self.fretboard):
                strung_notes = []
                for note_idx, note in enumerate(notes):
                    # need this for spacing
                    string_segment = f"{note:{'-' if string_idx < 3 else '='}<{self.fret_spacing[note_idx]}}"[
                        len(note) :
                    ]
                    styled_note = get_rgb_text(note)
                    styled_string_segment = get_rgb_text(string_segment)
                    if self.rgb_frets:
                        # set string color such that string to the left of note is same color as note
                        next_color = self.color_map[
                            self.chromatic_scale[
                                (self.chromatic_scale.index(note) + 1)
                                % len(self.chromatic_scale)
                            ]
                        ]
                        styled_note = get_rgb_text(note, self.color_map[note])
                        styled_string_segment = get_rgb_text(string_segment, next_color)
                    strung_notes.append(styled_note + styled_string_segment)
                strung_fretboard.append(strung_notes)
            headstock_copy = self.headstock.copy()
            # TODO: make this not so hard-coded
            start_idx = 0
            # extend the neck of the guitar
            headstock_copy[start_idx] += "".join(["_"] * sum(self.fret_spacing))
            for i, string in zip(range(start_idx + 1, start_idx + 7), strung_fretboard):
                headstock_copy[i] += "".join(string)
            rendered_fretboard = "\n".join(headstock_copy)

            # self.console.log(rendered_fretboard, markup=False)
            self.console.print(rendered_fretboard)
        except Exception as e:
            self.console.log(f"An unexpected error occurred: {e}")

    def set_chord(self, chord_name: str, variation: int) -> None:
        try:
            if chord_name.lower() not in [s.lower() for s in self.chord_names]:
                raise Exception(f"Chord {chord_name} not found!")
            # TODO: replace magic number
            if variation < 1 or variation > 6:
                raise Exception(
                    f"Variation {variation} for chord {chord_name} not found!"
                )
            self.chord = []
        except Exception as e:
            self.console.log(f"An unexpected error occurred: {e}")
