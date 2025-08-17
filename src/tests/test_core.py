from guitar_cli.core import Fretboard
from rich.console import Console


def test_show():
    fbs = [Fretboard(), Fretboard(rgb_frets=False)]
    for fb in fbs:
        fb.show()
        print()


if __name__ == "__main__":
    test_show()
