from rich.console import Console
from rich.padding import Padding
from rich.traceback import install

install()

c = Console()

test = Padding("this is text", style="on blue", expand=False)
c.print(test)

c.print("[rgb(240,0,0)]asd[rgb(0,240,240)]some text[/]")
