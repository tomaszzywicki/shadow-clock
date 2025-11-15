import typer
from .shadow_clock import shadow_clock


app = typer.Typer()
app.command()(shadow_clock)


if __name__ == "__main__":
    app()
