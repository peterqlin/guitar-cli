import re
import shutil
from rich.console import Console
from rich.text import Text
from .utils import (
    get_fret_spacing,
    get_rgb_text,
    get_bg_color_from_state,
    chromatic_scale,
    init_notes,
    color_map,
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
        self.fret_count = fret_count
        self.fret_spacing = get_fret_spacing(fretboard_length, fret_count)
        self.fretboard_window_width = shutil.get_terminal_size().columns
        self.fretboard_window_start = 0
        self.total_fretboard_width = 1000  # TODO: don't hard-code this
        self.state = {
            "display_mode": display_mode,
            "chord": [0] * 6,
            "find_note": "",
            "rgb_frets": rgb_frets,
            "labeled_frets": labeled_frets,
        }

        # TODO: allow toggle between equivalent sharps and flats

        self.valid_chord_names = set(["c", "cmaj"])

        self.chord_dict = {"c": [0, 1, 0, 2, 3, -1]}

        # TODO: maybe change how this is stored, but for now it'll work
        # get initial note positions, high e to low e
        init_pos = [chromatic_scale.index(n) for n in init_notes]
        # create fretboard with inc indices corresponding to lower pitch strings
        self.fretboard = [
            [
                chromatic_scale[
                    (i + pos + 1) % len(chromatic_scale)
                ]  # skip open string
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
        self.state["rgb_frets"] = not self.state["rgb_frets"]

    def toggle_labeled_frets(self) -> None:
        self.state["labeled_frets"] = not self.state["labeled_frets"]

    def pan_fretboard(self, direction: str, distance: int) -> None:
        if direction == "left":
            self.fretboard_window_start = max(self.fretboard_window_start - distance, 0)
        else:
            self.fretboard_window_start = min(
                self.fretboard_window_start + distance,
                self.total_fretboard_width - self.fretboard_window_width,
            )

    def render(self) -> Text:
        """
        Handle rendering the fretboard
        """
        fret = "┼"
        guitar_string = "───"
        fretboard_arr = [
            get_rgb_text(
                f'{(init_notes[string_idx] if self.state["labeled_frets"] else "─")}',
                bg_color=get_bg_color_from_state(
                    self.state, init_notes[string_idx], 0, string_idx
                ),
            )
            + fret
            + fret
            + fret.join(
                [
                    guitar_string
                    + get_rgb_text(
                        f'─{(note if self.state["labeled_frets"] else ""):─<2}',
                        bg_color=get_bg_color_from_state(
                            self.state, note, note_idx + 1, string_idx
                        ),  # add 1 because open string is not in notes array
                    )
                    + guitar_string
                    for note_idx, note in enumerate(notes)
                ]
            )
            for string_idx, notes in enumerate(self.fretboard)
        ]
        fretboard_arr.append(
            "   "
            + " ".join(
                [
                    (
                        "    .    "
                        if note_idx in [5, 7, 9, 15, 17]
                        else "    ..   " if note_idx == 12 else "         "
                    )
                    for note_idx in range(1, len(self.fretboard[0]))
                ]
            )
        )

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
        self.state["chord"] = self.chord_dict[chord_name]

    def set_find_note(self, find_note) -> None:
        self.state["find_note"] = find_note
