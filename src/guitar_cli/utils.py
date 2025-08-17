from rich.console import Console
class Fretboard:
    def __init__(self, fretboard_length=200, fret_count=12, rgb_frets=True, twelve_string=False) -> None:
        self.console = Console()        # create console for rich printing
        self.rgb_frets = rgb_frets      # toggle colored frets
        self.fret_spacing = get_fret_spacing(fretboard_length, fret_count)
        self.fill_char = "=" if twelve_string else "-"
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
        self.chord = [0] * 6 # initialize chord array
        
        chromatic_scale = ["c", "c#", "d", "d#", "e", "f", "f#", "g", "g#", "a", "a#", "b"] # initialize chromatic scale

        # TODO: maybe change how this is stored, but for now it'll work
        init_pos = [chromatic_scale.index(n) for n in ["e", "b", "g", "d", "a", "e"]]           # get initial note positions, high e to low e
        self.fretboard = [chromatic_scale[pos:] + chromatic_scale[:pos] for pos in init_pos]    # create fretboard with inc indices corresponding to lower pitch strings
    
    def show(self) -> None:
        """
        Handle rendering the fretboard
        """
        for frets in self.fretboard:
            if self.rgb_frets:
                frets = [
                    f"[rgb({self.color_map[f][0]},{self.color_map[f][1]},{self.color_map[f][2]})]{f:{self.fill_char}<{self.fret_spacing[i]}}[/]"
                    for i, f in enumerate(frets)
                ]
            else:
                frets = [
                    f"{f:{self.fill_char}<{self.fret_spacing[i]}}"
                    for i, f in enumerate(frets)
                ]
            self.console.print("".join(frets))
    
    def set_chord(self, chord: list[int]) -> None:
        self.chord = chord
    
    def set_fretboard_length(self, length: int) -> None:
        if length > 150:
            self.fretboard_length = length


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
