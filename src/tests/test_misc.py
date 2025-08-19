from guitar_cli.utils import styled_text_slice
from rich.console import Console

console = Console()

styled_text = "What is [i]your[/i] [bold red]name[/]? :smiley: "
sliced_text = styled_text_slice(styled_text, 0, 14)

console.print(sliced_text)
console.print(sliced_text, markup=False)
