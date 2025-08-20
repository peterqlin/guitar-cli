init_notes = ["e", "b", "g", "d", "a", "e"]

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
]

color_map = {
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


def get_rgb_text(
    text: str, fg_color: tuple | None = None, bg_color: tuple | None = None
) -> str:
    if not (fg_color or bg_color):
        return text
    style = ""
    if fg_color:
        r_f, g_f, b_f = fg_color
        style += f"[rgb({r_f},{g_f},{b_f})]"
    if bg_color:
        r_b, g_b, b_b = bg_color
        style += f"[on rgb({r_b},{g_b},{b_b})]"
    return f"{style}{text}[/]"


def get_dim_rgb(color: tuple, proportion: float) -> tuple:
    return tuple(round(v * proportion) for v in color)


def get_fret_spacing(scale_length: float, fret_count: int) -> list[int]:
    """
    Calculate the spacing between fret n and fret n+1 on a guitar.

    Args:
        scale_length (float): The scale length of the guitar (nut to bridge).
        fret_number (int): The fret number (0 = open string, 1 = first fret, etc.).

    Returns:
        int: The distance between fret n and fret n+1 rounded to the nearest integer.
    """
    return [
        round(scale_length * (1 / (2 ** (fret / 12)) - 1 / (2 ** ((fret + 1) / 12))))
        for fret in range(fret_count)
    ]


def step(note: str, delta: int) -> str:
    return chromatic_scale[(chromatic_scale.index(note) + delta) % len(chromatic_scale)]


def get_bg_color_from_state(
    state: dict, note: str, note_idx: int, string_idx: int
) -> tuple | None:
    if state["display_mode"] == "chord":
        if note_idx == state["chord"][string_idx]:
            return color_map[note] if state["rgb_frets"] else (240, 240, 240)
        return None
    if state["display_mode"] == "find":
        return color_map[note] if note == state["find_note"] else None
