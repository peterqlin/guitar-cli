from guitar_cli.core import Fretboard
from rich.console import Console
from rich.traceback import install

install()


def test_show():
    # fbs = [Fretboard(), Fretboard(rgb_frets=False)]
    # for fb in fbs:
    #     fb.show()
    f = Fretboard()
    f.show()


if __name__ == "__main__":
    test_show()
