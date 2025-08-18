def get_rgb_text(text: str, rgb_color: tuple = (240, 240, 240)) -> str:
    r, g, b = rgb_color
    return f"[rgb({r},{g},{b})]{text}[/]"


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
