"""Tests the solution of the challenge for Day 2."""
from pathlib import Path

import pytest

from days.day_02 import Round, OpponentChoice, PlayerChoice

INPUT_FILE_PATH = Path(__file__).parent.joinpath(
    "input-files", "day-02-simple.txt")


@pytest.mark.parametrize(
    "input_line,expected_game",
    zip(
        INPUT_FILE_PATH.open(mode="r").readlines(),
        [
            Round(
                opponent_choice=OpponentChoice.ROCK,
                player_choice=PlayerChoice.PAPER,
            ),
            Round(
                opponent_choice=OpponentChoice.PAPER,
                player_choice=PlayerChoice.ROCK,
            ),
            Round(
                opponent_choice=OpponentChoice.SCISSORS,
                player_choice=PlayerChoice.SCISSORS,
            ),
        ]
    )
)
def test_game_from_string(input_line: str, expected_game: Round) -> None:
    """
    Verify the from_string method of Round works as intended.

    :param input_line: A line from a file that defines a move by an opponent
        followed by a move from a player
    :type input_line: str
    :param expected_game: The Round object we expect the from_string method to
        create
    :type expected_game: Round
    """
    actual_game = Round.from_string(input_string=input_line, split_string=" ")
    assert actual_game == expected_game
