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


def get_fret_dimness(display_mode: str, **kwargs) -> float:
    if display_mode == "chord":
        return 1 if kwargs["note_idx"] == kwargs["chord_idx"] else 0
    if display_mode == "find":
        return 1 if kwargs["note"] == kwargs["find_note"] else 0
    raise Exception("Invalid display mode!")


def step(note: str, delta: int) -> str:
    return chromatic_scale[(chromatic_scale.index(note) + delta) % len(chromatic_scale)]


def styled_text_slice(styled_text: str, start: int, end: int) -> str:
    sliced = ""
    nonstyled_count = start
    i = 0
    # TODO: brackets in the ascii art could break this
    # TODO: slicing out entire style chunks could break this
    while nonstyled_count < end:
        sliced += styled_text[i]
        if styled_text[i] == "[":
            while styled_text[i] != "]":
                sliced += styled_text[i]
                i += 1
        else:
            nonstyled_count += 1
        i += 1
    return sliced
