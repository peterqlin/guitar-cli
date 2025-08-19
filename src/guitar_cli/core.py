from rich.console import Console
from rich.text import Text
from .utils import get_fret_spacing, get_rgb_text, dim_rgb


class Fretboard:
    def __init__(
        self, fretboard_length=200, fret_count=12, rgb_frets=True, labeled_frets=True
    ) -> None:
        self.console = Console()
        self.rgb_frets = rgb_frets
        self.labeled_frets = labeled_frets
        self.fret_count = fret_count
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

        self.valid_chord_names = set(["c", "cmaj"])

        self.chord_dict = {"c": [0, 1, 0, 2, 3, -1]}

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
                # TODO: add underline to second-to-last row
                # set color of ascii art to white
                # self.headstock = [
                #     get_rgb_text(line.rstrip("\n"), fg_color=(240, 240, 240))
                #     for line in f
                # ]
                self.headstock = f.read()
        except Exception as e:
            self.console.log(f"Failed to load headstock ASCII art: {e}")
            self.headstock = ""

    def toggle_rgb_frets(self) -> None:
        self.rgb_frets = not self.rgb_frets

    def show(self) -> Text:
        """
        Handle rendering the fretboard
        """
        # TODO: make it customizable (yes/no rgb, etc)
        # try:
        # self.console.clear()
        white_rgb = (240, 240, 240)
        gray_rgb = (150, 150, 150)
        black_rgb = (0, 0, 0)

        styled_fret = get_rgb_text(" ", bg_color=gray_rgb)
        fretboard_arr = [
            styled_fret.join(
                [
                    get_rgb_text(
                        (f"    {note: <2}   " if note_idx > 0 else f" {note: <2}"),
                        bg_color=dim_rgb(
                            (self.color_map[note] if self.rgb_frets else white_rgb),
                            1 if self.chord[string_idx] == note_idx else 0,
                        ),
                    )
                    for note_idx, note in enumerate(notes)
                ]
            )
            for string_idx, notes in enumerate(self.fretboard)
        ]

        rendered_fretboard = "\n".join(fretboard_arr)

        # self.console.print("\n" + rendered_fretboard + "\n")
        return Text.from_markup("\n" + rendered_fretboard + "\n")
        # except Exception as e:
        # self.console.log(f"An unexpected error occurred: {e}")

    def set_chord(self, chord_name: str, variation: int) -> None:
        try:
            chord_name = chord_name.strip().lower()
            if chord_name not in [s.lower() for s in self.valid_chord_names]:
                raise Exception(f"Chord {chord_name} not found!")
            # TODO: replace magic number
            if variation < 1 or variation > 6:
                raise Exception(
                    f"Variation {variation} for chord {chord_name} not found!"
                )
            self.chord = self.chord_dict[chord_name]
        except Exception as e:
            self.console.log(f"An unexpected error occurred: {e}")
