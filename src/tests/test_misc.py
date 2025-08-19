from rich.text import Text
from rich.console import Console

console = Console()

styled_text = Text.from_markup("What is [i]your[/i] [bold red]name[/]? :smiley: ")

console.print(styled_text)
console.print(styled_text, markup=False)
