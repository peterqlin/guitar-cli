from rich.text import Text
from rich.console import Console
from rich.padding import Padding
from rich.traceback import install

install()

c = Console()

test = Padding("this is text", style="on blue", expand=False)
c.print(test)

c.print("[rgb(240,0,0)]asd[rgb(0,240,240)]some text[/]")
c.print("[white underline]asd[rgb(0,240,240)]some text[/]")

text = Text("Hello, World!", style="red")  # Text color
text.stylize("underline blue", 0, len(text))  # Underline in a different color

c.print(text)
