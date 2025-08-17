from guitar_cli.core import Fretboard


def test_show():
    f1 = Fretboard()
    f2 = Fretboard(rgb_frets=False)

    f1.show()
    f2.show()


if __name__ == "__main__":
    test_show()
