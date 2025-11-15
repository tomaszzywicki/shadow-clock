import time as time
from datetime import datetime
from rich.live import Live
from rich.align import Align
from rich.text import Text

from .console import console


def shadow_clock():
    with Live(console=console, screen=True) as live:
        while True:
            time_now = datetime.now()
            ascii_time = time_to_ascii_string(time_now)

            terminal_height = console.size.height

            text_lines = ascii_time.count("\n") + 1
            vertical_padding = max(0, (terminal_height - text_lines) // 2)

            padded_text = "\n" * vertical_padding + ascii_time

            text = Text(padded_text, style="red")
            align = Align.center(text, vertical="middle")

            live.update(align)
            time.sleep(0.1)


DIGITS = {
    0: """ ██████╗ \n██╔═████╗\n██║██╔██║\n████╔╝██║\n╚██████╔╝\n ╚═════╝ """,
    1: """ ██╗\n███║\n╚██║\n ██║\n ██║\n ╚═╝""",
    2: """██████╗ \n╚════██╗\n █████╔╝\n██╔═══╝ \n███████╗\n╚══════╝""",
    3: """██████╗ \n╚════██╗\n █████╔╝\n ╚═══██╗\n██████╔╝\n╚═════╝ """,
    4: """██╗  ██╗\n██║  ██║\n███████║\n╚════██║\n     ██║\n     ╚═╝""",
    5: """███████╗\n██╔════╝\n███████╗\n╚════██║\n███████║\n╚══════╝""",
    6: """ ██████╗ \n██╔════╝ \n███████╗ \n██╔═══██╗\n╚██████╔╝\n ╚═════╝ """,
    7: """███████╗\n╚════██║\n    ██╔╝\n   ██╔╝ \n   ██║  \n   ╚═╝  """,
    8: """ █████╗ \n██╔══██╗\n╚█████╔╝\n██╔══██╗\n╚█████╔╝\n ╚════╝ """,
    9: """ █████╗ \n██╔══██╗\n╚██████║\n ╚═══██║\n █████╔╝\n ╚════╝ """,
    "colon": """   \n██╗\n╚═╝\n██╗\n╚═╝\n   """,
}

DIGIT_HEIGHT = 6


def _time_to_digit_list(time: datetime):
    hour = f"{time.hour:02d}"
    minute = f"{time.minute:02d}"

    return [int(hour[0]), int(hour[1]), int(minute[0]), int(minute[1])]


def _digit_list_to_splitted_lines(digit_list: list[int]) -> list[str]:
    splitted_lines = []
    for digit in digit_list:
        digit = DIGITS[digit].split("\n")
        splitted_lines.append(digit)
    splitted_lines.insert(2, DIGITS["colon"].split("\n"))
    return splitted_lines


def _ascii_hour_from_splitted_lines(letters_lines: list[str]) -> str:
    result = ""
    for line in range(DIGIT_HEIGHT):
        for letter_line in letters_lines:
            result += letter_line[line]
            result += " "
        result += " \n"
    return result


def time_to_ascii_string(time: datetime):
    digit_list = _time_to_digit_list(time)
    splitted_lines = _digit_list_to_splitted_lines(digit_list)
    ascii_hour = _ascii_hour_from_splitted_lines(splitted_lines)
    return ascii_hour
