from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from .solar import HFWatch


console = Console()


def main():

    hf = HFWatch()

    with console.status("[bold green]Fetching solar conditions..."):
        hf.update()


    console.print()


    title = Text(
        "☀ HF WATCH",
        justify="center",
        style="bold cyan"
    )

    console.print(
        Panel(
            title,
            subtitle="HF Propagation Monitor",
        )
    )


    console.print()


    status = Table(
        title="Solar Conditions",
        show_header=False,
        box=None
    )

    status.add_row(
        "Solar Flux Index",
        str(hf.sfi)
    )

    status.add_row(
        "K Index",
        str(hf.k)
    )

    status.add_row(
        "A Index",
        str(hf.a)
    )


    console.print(status)


    console.print()


    condition_style = {
        "GOOD": "green",
        "FAIR": "yellow",
        "POOR": "orange3",
        "BAD": "red",
        "NO DATA": "grey50"
    }


    colour = condition_style.get(
        hf.condition,
        "white"
    )


    console.print(
        Panel(
            Text(
                hf.condition,
                style=f"bold {colour}",
                justify="center"
            ),
            title="Band Conditions"
        )
    )


    bands = Table()

    bands.add_column(
        "Band",
        style="cyan"
    )

    bands.add_column(
        "Status",
        justify="center"
    )


    for band, value in hf.bands.items():

        style = condition_style.get(
            value,
            "white"
        )

        bands.add_row(
            band,
            Text(
                value,
                style=style
            )
        )


    console.print(bands)

    console.print()


if __name__ == "__main__":
    main()
