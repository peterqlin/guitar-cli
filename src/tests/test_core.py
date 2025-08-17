from guitar_cli.core import Fretboard
from rich.console import Console


def test_show():
    fb1 = Fretboard()
    fb2 = Fretboard(rgb_frets=False)
    fb3 = Fretboard(twelve_string=True)
    fb4 = Fretboard(rgb_frets=False, twelve_string=True)

    fbs = [fb1, fb2, fb3, fb4]
    for fb in fbs:
        fb.show()
        print()


if __name__ == "__main__":
    test_show()
