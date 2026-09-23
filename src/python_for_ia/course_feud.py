"""Facilitator-only Course Feud terminal game."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path

from rich import box
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

DEFAULT_ANSWERS_PATH = Path("course_feud_answers.json")
MATCH_THRESHOLD = 0.58


@dataclass(frozen=True)
class Answer:
    text: str
    aliases: tuple[str, ...]
    points: int


@dataclass(frozen=True)
class Module:
    number: str
    title: str
    answers: tuple[Answer, ...]


def normalize(value: str) -> str:
    """Normalize an answer for forgiving comparisons."""
    return " ".join(re.sub(r"[^\w\s]", " ", value.casefold()).split())


def similarity(guess: str, expected: str) -> float:
    """Score a guess against an answer or alias."""
    normalized_guess = normalize(guess)
    normalized_expected = normalize(expected)
    if not normalized_guess or not normalized_expected:
        return 0.0
    if normalized_guess == normalized_expected:
        return 1.0

    guess_words = set(normalized_guess.split())
    expected_words = set(normalized_expected.split())
    overlap = len(guess_words & expected_words) / min(
        len(guess_words), len(expected_words)
    )
    sequence = SequenceMatcher(None, normalized_guess, normalized_expected).ratio()
    return max(overlap, sequence)


def load_modules(path: Path) -> dict[str, Module]:
    """Load and validate modules from an editable JSON file."""
    try:
        raw_modules = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise ValueError(f"Answer file not found: {path}") from error
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid JSON in {path}: {error}") from error

    if not isinstance(raw_modules, dict) or not raw_modules:
        raise ValueError("The answer file must contain at least one module.")

    modules: dict[str, Module] = {}
    for number, raw_module in raw_modules.items():
        try:
            title = str(raw_module["title"])
            raw_answers = raw_module["answers"]
            answers = tuple(
                Answer(
                    text=str(raw_answer["answer"]),
                    aliases=tuple(
                        str(alias) for alias in raw_answer.get("aliases", [])
                    ),
                    points=int(raw_answer.get("points", 0)),
                )
                for raw_answer in raw_answers
            )
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError(f"Invalid definition for module {number!r}.") from error
        if not answers:
            raise ValueError(f"Module {number!r} must contain at least one answer.")
        modules[str(number)] = Module(str(number), title, answers)
    return modules


class CourseFeud:
    """Render a board and process facilitator commands."""

    def __init__(
        self,
        modules: dict[str, Module],
        module_number: str,
        *,
        console: Console,
        clear_screen: bool = True,
    ) -> None:
        self.modules = modules
        self.console = console
        self.clear_screen = clear_screen
        self.module = self._get_module(module_number)
        self.revealed: set[int] = set()

    def _get_module(self, number: str) -> Module:
        try:
            return self.modules[number]
        except KeyError as error:
            available = ", ".join(sorted(self.modules, key=int))
            raise ValueError(
                f"Unknown module {number!r}. Available modules: {available}."
            ) from error

    def render(self, message: str | None = None) -> None:
        if self.clear_screen:
            self.console.clear()

        heading = Text("COURSE FEUD", style="bold bright_yellow", justify="center")
        subtitle = Text(
            f"Module {self.module.number}: {self.module.title}",
            style="bold bright_cyan",
            justify="center",
        )
        self.console.print(Panel(Align.center(Text.assemble(heading, "\n", subtitle))))

        table = Table(
            box=box.DOUBLE_EDGE,
            border_style="bright_blue",
            show_header=False,
            expand=True,
            padding=(0, 1),
        )
        table.add_column("Rank", width=5, justify="center", style="bold yellow")
        table.add_column("Answer", ratio=1)
        table.add_column("Points", width=8, justify="center", style="bold yellow")

        for rank, answer in enumerate(self.module.answers, start=1):
            if rank - 1 in self.revealed:
                answer_text = Text(answer.text, style="bold white")
                points = str(answer.points)
            else:
                answer_text = Text("▰ " * 12, style="blue")
                points = "?"
            table.add_row(str(rank), answer_text, points)

        self.console.print(table)
        if message:
            self.console.print(Panel(message, border_style="magenta"))
        self.console.print(
            "[dim]/reveal <answer>  /show  /move <module_number>  /reset  /quit[/dim]"
        )

    def reveal(self, guess: str) -> str:
        best_index = -1
        best_score = 0.0
        for index, answer in enumerate(self.module.answers):
            candidates = (answer.text, *answer.aliases)
            score = max(similarity(guess, candidate) for candidate in candidates)
            if score > best_score:
                best_index = index
                best_score = score

        if best_index < 0 or best_score < MATCH_THRESHOLD:
            return f"❌ No prepared answer matched [bold]{guess}[/bold]. Try another phrase."
        if best_index in self.revealed:
            return f"Answer {best_index + 1} is already on the board."

        self.revealed.add(best_index)
        answer = self.module.answers[best_index]
        return f"🔔 Survey says… [bold bright_green]{answer.text}[/bold bright_green]!"

    def process(self, command: str) -> tuple[bool, str | None]:
        command = command.strip()
        if not command:
            return True, None

        name, _, argument = command.partition(" ")
        argument = argument.strip()

        if name == "/reveal":
            if not argument:
                return True, "Usage: [bold]/reveal <answer>[/bold]"
            return True, self.reveal(argument)
        if name == "/show":
            self.revealed = set(range(len(self.module.answers)))
            return True, "All answers revealed."
        if name == "/move":
            if not argument:
                return True, "Usage: [bold]/move <module_number>[/bold]"
            try:
                self.module = self._get_module(argument)
            except ValueError as error:
                return True, str(error)
            self.revealed.clear()
            return True, f"Moved to module {argument}. The board has been reset."
        if name == "/reset":
            self.revealed.clear()
            return True, "Board reset."
        if name == "/quit":
            return False, None
        return True, f"Unknown command: [bold]{name}[/bold]"

    def run(self) -> None:
        message: str | None = None
        while True:
            self.render(message)
            try:
                command = self.console.input("\n[bold cyan]Host>[/bold cyan] ")
            except (EOFError, KeyboardInterrupt):
                self.console.print("\nThanks for playing!")
                return
            keep_running, message = self.process(command)
            if not keep_running:
                self.console.print("Thanks for playing!")
                return


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the Course Feud classroom board.")
    parser.add_argument(
        "module",
        nargs="?",
        default="1",
        help="module number to show initially (default: 1)",
    )
    parser.add_argument(
        "--answers",
        type=Path,
        default=DEFAULT_ANSWERS_PATH,
        help=f"answer file (default: {DEFAULT_ANSWERS_PATH})",
    )
    parser.add_argument(
        "--no-clear",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    console = Console()
    try:
        modules = load_modules(args.answers)
        game = CourseFeud(
            modules,
            args.module,
            console=console,
            clear_screen=not args.no_clear,
        )
    except ValueError as error:
        console.print(f"[bold red]Error:[/bold red] {error}")
        raise SystemExit(2) from error
    game.run()


if __name__ == "__main__":
    main()
