from rich.console import Console
class Fretboard:
    def __init__(self):
        self.console = Console()
        self.fretboard_length = 200
        # TODO: make the color difference between sharp and natural notes more obvious
        self.color_map = {
            'e': (228, 3, 3),       # Red
            'f': (255, 140, 0),     # Orange
            'f#': (255, 165, 0),
            'g': (255, 237, 0),     # Yellow
            'g#': (255, 252, 0),
            'a': (0, 128, 38),      # Green
            'a#': (0, 143, 53),
            'b': (0, 77, 255),      # Blue
            'c': (75, 0, 130),      # Indigo
            'c#': (90, 0, 145),
            'd': (117, 7, 135),     # Violet
            'd#': (132, 7, 150)
        }

        for note, (r,g,b) in self.color_map.items():
            self.console.print(f"[rgb({r},{g},{b})]{note}[/]")


def get_fret_spacing(scale_length: float, fret_count: int) -> list[int]:
    """
    Calculate the spacing between fret n and fret n+1 on a guitar.
    
    Args:
        scale_length (float): The scale length of the guitar (nut to bridge).
        fret_number (int): The fret number (0 = open string, 1 = first fret, etc.).
        
    Returns:
        int: The distance between fret n and fret n+1 rounded to the nearest integer.
    """
    return [round(scale_length * (1 / (2 ** (fret / 12)) - 1 / (2 ** ((fret + 1) / 12)))) for fret in range(fret_count)]
