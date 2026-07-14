from datetime import datetime, timezone

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.align import Align

from .solar import HFWatch


console = Console()


def condition_colour(value):

    colours = {
        "GOOD": "green",
        "EXCELLENT": "bold green",
        "FAIR": "yellow",
        "POOR": "orange3",
        "LOW": "red",
        "BAD": "bold red",
        "NO DATA": "grey50",
    }

    return colours.get(value, "white")



def propagation_score(hf):

    try:
        sfi = int(hf.sfi)
        k = int(hf.k)
        a = int(hf.a)

    except ValueError:
        return 0


    score = 50


    if sfi >= 150:
        score += 20
    elif sfi >= 100:
        score += 10


    if k <= 2:
        score += 15
    elif k >= 5:
        score -= 20


    if a <= 10:
        score += 15
    elif a > 20:
        score -= 15


    return max(0, min(score, 100))



def progress_bar(score):

    blocks = int(score / 10)

    return (
        "█" * blocks +
        "░" * (10 - blocks)
        +
        f" {score}%"
    )



def main():

    hf = HFWatch()


    with console.status(
        "[bold cyan]Contacting solar data service..."
    ):
        hf.update()



    console.clear()


    console.print(
        Panel(
            Align.center(
                Text(
                    "📡 HF WATCH\n"
                    "Amateur Radio Propagation Monitor",
                    style="bold cyan"
                )
            )
        )
    )


    console.print()


    solar = Table(
        title="☀ Solar Conditions",
        expand=True
    )

    solar.add_column(
        "Parameter",
        style="cyan"
    )

    solar.add_column(
        "Value",
        justify="right"
    )


    solar.add_row(
        "Solar Flux Index",
        str(hf.sfi)
    )

    solar.add_row(
        "K Index",
        str(hf.k)
    )

    solar.add_row(
        "A Index",
        str(hf.a)
    )


    solar.add_row(
        "UTC Time",
        datetime.now(
            timezone.utc
        ).strftime(
            "%Y-%m-%d %H:%M"
        )
    )


    console.print(solar)


    console.print()


    score = propagation_score(hf)


    console.print(
        Panel(
            Text(
                progress_bar(score),
                justify="center",
                style="bold green"
            ),
            title="📈 Propagation Score"
        )
    )


    console.print()


    status = Text(
        hf.condition,
        style=f"bold {condition_colour(hf.condition)}"
    )


    console.print(
        Panel(
            Align.center(status),
            title="Overall Conditions"
        )
    )


    console.print()


    bands = Table(
        title="📻 Band Conditions",
        expand=True
    )


    bands.add_column(
        "Band",
        style="cyan"
    )

    bands.add_column(
        "Status",
        justify="center"
    )



    for band, condition in hf.bands.items():

        bands.add_row(
            band,
            Text(
                condition,
                style=condition_colour(condition)
            )
        )


    console.print(bands)


    console.print()

    console.print(
        "[dim]HF Watch - amateur radio propagation tool[/dim]"
    )



if __name__ == "__main__":
    main()
