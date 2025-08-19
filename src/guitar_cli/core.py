import re
import shutil
from rich.console import Console
from rich.text import Text
from .utils import (
    get_fret_spacing,
    get_fret_dimness,
    get_rgb_text,
    get_dim_rgb,
    chromatic_scale,
    init_notes,
)


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
        self.fretboard_window_width = shutil.get_terminal_size().columns
        self.fretboard_window_start = 0
        self.total_fretboard_width = 1000  # TODO: don't hard-code this
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
        init_pos = [chromatic_scale.index(n) for n in init_notes]
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
            with open("assets/fender_strat_headstock.txt", "r", encoding="utf-8") as f:
                self.headstock = f.read()
        except Exception as e:
            self.console.log(f"Failed to load headstock ASCII art: {e}")
            self.headstock = ""

    def toggle_rgb_frets(self) -> None:
        self.rgb_frets = not self.rgb_frets

    def toggle_labeled_frets(self) -> None:
        self.labeled_frets = not self.labeled_frets

    def pan_fretboard(self, delta: int) -> None:
        new_window_start = self.fretboard_window_start + delta
        if delta < 0:
            self.fretboard_window_start = max(new_window_start, 0)
        else:
            self.fretboard_window_start = min(
                new_window_start,
                self.total_fretboard_width - self.fretboard_window_width,
            )

    def render(self) -> Text:
        """
        Handle rendering the fretboard
        """
        white_rgb = (240, 240, 240)
        gray_rgb = (150, 150, 150)
        black_rgb = (0, 0, 0)

        styled_fret = get_rgb_text("┼", bg_color=black_rgb)
        styled_string = get_rgb_text("───", bg_color=black_rgb)
        fretboard_arr = [
            get_rgb_text(
                f"{(init_notes[string_idx] if self.labeled_frets else "─")}",
                bg_color=get_dim_rgb(
                    (
                        self.color_map[init_notes[string_idx]]
                        if self.rgb_frets
                        else white_rgb
                    ),
                    get_fret_dimness(
                        self.display_mode,
                        note=init_notes[string_idx],
                        note_idx=0,
                        chord_idx=self.chord[string_idx],
                        find_note=self.find_note,
                    ),
                ),
            )
            + styled_fret
            + styled_fret
            + styled_fret.join(
                [
                    styled_string
                    + get_rgb_text(
                        f"─{(note if self.labeled_frets else ""):─<2}",
                        bg_color=get_dim_rgb(
                            (self.color_map[note] if self.rgb_frets else white_rgb),
                            get_fret_dimness(
                                self.display_mode,
                                note=note,
                                note_idx=note_idx + 1,
                                chord_idx=self.chord[string_idx],
                                find_note=self.find_note,
                            ),
                        ),
                    )
                    + styled_string
                    for note_idx, note in enumerate(notes[1:])
                ]
            )
            for string_idx, notes in enumerate(self.fretboard)
        ]

        replacements = {
            f"({i})": styled_string for i, styled_string in enumerate(fretboard_arr)
        }
        pattern = re.compile("|".join(map(re.escape, replacements.keys())))
        rendered_fretboard = pattern.sub(
            lambda m: replacements[m.group(0)], self.headstock
        )

        rendered_fretboard_segment = Text()
        for line in rendered_fretboard.split("\n"):
            rendered_fretboard_segment += (
                Text.from_markup(line)[
                    self.fretboard_window_start : self.fretboard_window_start
                    + self.fretboard_window_width
                ]
                + "\n"
            )

        return rendered_fretboard_segment

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
