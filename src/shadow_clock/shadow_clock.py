import typer
import time as time
from datetime import datetime
from rich.live import Live
from rich.align import Align
from rich.text import Text
from typing_extensions import Annotated

from .console import console


def shadow_clock(
    include_seconds: Annotated[
        bool,
        typer.Option("--second", "-s", help="Display the clock with seconds"),
    ] = False,
    color: Annotated[
        str, typer.Option("--color", "-c", help="Set the string color (could be like '#2064be' or blue)")
    ] = "blue",
):
    with Live(console=console, screen=True) as live:
        while True:
            time_now = datetime.now()
            ascii_time = time_to_ascii_string(time_now, include_seconds)

            terminal_height = console.size.height
            text_lines = ascii_time.count("\n") + 1
            vertical_padding = max(0, (terminal_height - text_lines) // 2)
            padded_text = "\n" * vertical_padding + ascii_time

            text = Text(padded_text, style=color)
            align = Align.center(text, vertical="middle")

            live.update(align, refresh=True)
            sleep_duration = 1.0 - (time_now.microsecond / 1_000_000.0) + 0.01
            time.sleep(sleep_duration)


DIGITS = {
    0: """ ██████╗ \n██╔═████╗\n██║██╔██║\n████╔╝██║\n╚██████╔╝\n ╚═════╝ """,
    1: """    ██╗  \n   ███║  \n   ╚██║  \n    ██║  \n    ██║  \n    ╚═╝  """,
    2: """██████╗  \n╚════██╗ \n █████╔╝ \n██╔═══╝  \n███████╗ \n╚══════╝ """,
    3: """██████╗  \n╚════██╗ \n █████╔╝ \n ╚═══██╗ \n██████╔╝ \n╚═════╝  """,
    4: """██╗  ██╗ \n██║  ██║ \n███████║ \n╚════██║ \n     ██║ \n     ╚═╝ """,
    5: """███████╗ \n██╔════╝ \n███████╗ \n╚════██║ \n███████║ \n╚══════╝ """,
    6: """ ██████╗ \n██╔════╝ \n███████╗ \n██╔═══██╗\n╚██████╔╝\n ╚═════╝ """,
    7: """███████╗ \n╚════██║ \n    ██╔╝ \n   ██╔╝  \n   ██║   \n   ╚═╝   """,
    8: """ █████╗  \n██╔══██╗ \n╚█████╔╝ \n██╔══██╗ \n╚█████╔╝ \n ╚════╝  """,
    9: """ █████╗  \n██╔══██╗ \n╚██████║ \n ╚═══██║ \n █████╔╝ \n ╚════╝  """,
    "colon": """   \n██╗\n╚═╝\n██╗\n╚═╝\n   """,
}


DIGIT_HEIGHT = 6


def _time_to_digit_list(time: datetime, include_seconds: bool = False):
    hour = f"{time.hour:02d}"
    minute = f"{time.minute:02d}"
    if include_seconds:
        second = f"{time.second:02d}"
        return [int(hour[0]), int(hour[1]), int(minute[0]), int(minute[1]), int(second[0]), int(second[1])]

    return [int(hour[0]), int(hour[1]), int(minute[0]), int(minute[1])]


def _digit_list_to_splitted_lines(digit_list: list[int]) -> list[str]:
    n = len(digit_list)
    splitted_lines = []
    for digit in digit_list:
        digit = DIGITS[digit].split("\n")
        splitted_lines.append(digit)
    splitted_lines.insert(2, DIGITS["colon"].split("\n"))
    if n > 4:
        splitted_lines.insert(5, DIGITS["colon"].split("\n"))
    return splitted_lines


def _ascii_hour_from_splitted_lines(letters_lines: list[str]) -> str:
    result = ""
    for line in range(DIGIT_HEIGHT):
        for letter_line in letters_lines:
            result += letter_line[line]
            result += " "
        result += " \n"
    return result


def time_to_ascii_string(time: datetime, include_seconds: bool = False):
    digit_list = _time_to_digit_list(time, include_seconds)
    splitted_lines = _digit_list_to_splitted_lines(digit_list)
    ascii_hour = _ascii_hour_from_splitted_lines(splitted_lines)
    return ascii_hour
