from rich.console import Console
from rich.text import Text
from .utils import get_fret_spacing, get_rgb_text, dim_rgb, chromatic_scale


class Fretboard:
    def __init__(
        self,
        display_mode,
        fretboard_length=200,
        fret_count=12,
        rgb_frets=True,
        labeled_frets=True,
    ) -> None:
        self.console = Console()
        self.rgb_frets = rgb_frets
        self.labeled_frets = labeled_frets
        self.fret_count = fret_count
        self.fret_spacing = get_fret_spacing(fretboard_length, fret_count)
        self.display_mode = display_mode
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
        self.find_note = "e"

        # TODO: allow toggle between equivalent sharps and flats

        self.valid_chord_names = set(["c", "cmaj"])

        self.chord_dict = {"c": [0, 1, 0, 2, 3, -1]}

        # TODO: maybe change how this is stored, but for now it'll work
        # get initial note positions, high e to low e
        init_pos = [chromatic_scale.index(n) for n in ["e", "b", "g", "d", "a", "e"]]
        # TODO: fix bug where zooming in and out causes visual glitches
        # TODO: add scrolling when fretboard doesn't fit in terminal
        # create fretboard with inc indices corresponding to lower pitch strings
        self.fretboard = [
            [
                chromatic_scale[(i + pos) % len(chromatic_scale)]
                for i in range(self.fret_count)
            ]
            for pos in init_pos
        ]

        try:
            with open(
                "src/guitar_cli/headstock_ascii_art.txt", "r", encoding="utf-8"
            ) as f:
                self.headstock = f.read()
        except Exception as e:
            self.console.log(f"Failed to load headstock ASCII art: {e}")
            self.headstock = ""

    def toggle_rgb_frets(self) -> None:
        self.rgb_frets = not self.rgb_frets

    def toggle_labeled_frets(self) -> None:
        self.labeled_frets = not self.labeled_frets

    def render(self) -> Text:
        """
        Handle rendering the fretboard
        """
        white_rgb = (240, 240, 240)
        gray_rgb = (150, 150, 150)
        black_rgb = (0, 0, 0)

        styled_fret = get_rgb_text("┼", bg_color=black_rgb)
        fretboard_arr = [
            styled_fret.join(
                [
                    get_rgb_text(
                        (
                            f"────{(note if self.labeled_frets else ""):─<2}───"
                            if note_idx > 0
                            else f"─{(note if self.labeled_frets else ""):─<2}"
                        ),
                        bg_color=dim_rgb(
                            (self.color_map[note] if self.rgb_frets else white_rgb),
                            (
                                (1 if note_idx == self.chord[string_idx] else 0)
                                if self.display_mode
                                == "chord"  # TODO: add an elif for `find` mode
                                else (1 if note == self.find_note else 0)
                            ),
                        ),
                    )
                    for note_idx, note in enumerate(notes)
                ]
            )
            for string_idx, notes in enumerate(self.fretboard)
        ]

        rendered_fretboard = "\n".join(fretboard_arr)

        return Text.from_markup("\n" + rendered_fretboard + "\n")

    def set_chord(self, chord_name: str, variation: int) -> None:
        chord_name = chord_name.strip().lower()
        if chord_name not in [s.lower() for s in self.valid_chord_names]:
            raise Exception(f"Chord {chord_name} not found!")
        # TODO: replace magic number
        if variation < 1 or variation > 6:
            raise Exception(f"Variation {variation} for chord {chord_name} not found!")
        self.chord = self.chord_dict[chord_name]

    def set_find_note(self, find_note) -> None:
        self.find_note = find_note
