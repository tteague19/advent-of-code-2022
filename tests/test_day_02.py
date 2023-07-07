"""Tests the solution of the challenge for Day 2."""
from itertools import repeat
from pathlib import Path

import pytest

from days.day_02 import Round, OpponentChoice, PlayerChoice, RoundOutcome, \
    RoundScore, PLAYER_SELECTION_TO_SCORE_DICT, SelectionScore

INPUT_FILE_PATH = Path(__file__).parent.joinpath(
    "input-files", "day-02-simple.txt")


@pytest.mark.parametrize(
    "input_line,expected_round",
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
def test_round_from_string(input_line: str, expected_round: Round) -> None:
    """
    Verify the from_string method of Round works as intended.

    :param input_line: A line from a file that defines a move by an opponent
        followed by a move from a player
    :type input_line: str
    :param expected_round: The Round object we expect the from_string method to
        create
    :type expected_round: Round
    """
    actual_round = Round.from_string(input_string=input_line, split_string=" ")
    assert actual_round == expected_round


@pytest.mark.parametrize(
    "round_obj,expected_outcome",
    zip(
        [
            Round(
                opponent_choice=OpponentChoice.ROCK,
                player_choice=PlayerChoice.ROCK,
            ),
            Round(
                opponent_choice=OpponentChoice.SCISSORS,
                player_choice=PlayerChoice.SCISSORS,
            ),
            Round(
                opponent_choice=OpponentChoice.PAPER,
                player_choice=PlayerChoice.PAPER,
            ),
            Round(
                opponent_choice=OpponentChoice.SCISSORS,
                player_choice=PlayerChoice.ROCK,
            ),
            Round(
                opponent_choice=OpponentChoice.ROCK,
                player_choice=PlayerChoice.PAPER,
            ),
            Round(
                opponent_choice=OpponentChoice.PAPER,
                player_choice=PlayerChoice.SCISSORS,
            ),
            Round(
                opponent_choice=OpponentChoice.ROCK,
                player_choice=PlayerChoice.SCISSORS,
            ),
            Round(
                opponent_choice=OpponentChoice.PAPER,
                player_choice=PlayerChoice.ROCK,
            ),
            Round(
                opponent_choice=OpponentChoice.SCISSORS,
                player_choice=PlayerChoice.PAPER,
            ),
        ],
        [
            RoundOutcome.DRAW,
            RoundOutcome.DRAW,
            RoundOutcome.DRAW,
            RoundOutcome.WIN,
            RoundOutcome.WIN,
            RoundOutcome.WIN,
            RoundOutcome.LOSS,
            RoundOutcome.LOSS,
            RoundOutcome.LOSS,
        ]
    )
)
def test_round_determine_outcome(
        round_obj: Round, expected_outcome: RoundOutcome) -> None:
    """
    Verify determine_outcome method of Round computes the appropriate outcome.

    :param round_obj: An object that represents a round of play in a game of
        Rock Paper Scissors
    :type round_obj: Round
    :param expected_outcome: The outcome we expect the :param:`round_obj`
        to produce
    :type expected_outcome: RoundOutcome
    """
    actual_outcome = round_obj.determine_outcome()
    assert actual_outcome == expected_outcome


@pytest.mark.parametrize(
    "input_line,expected_score,selection_score_dict",
    zip(
        INPUT_FILE_PATH.open(mode="r").readlines(),
        [8, 1, 6],
        repeat(PLAYER_SELECTION_TO_SCORE_DICT, 3),
    )
)
def test_round_compute_score(
        input_line: str,
        expected_score: RoundScore,
        selection_score_dict: dict[PlayerChoice, SelectionScore],
) -> None:
    """
    Compare an expected score for each round to the output from a method.

    :param input_line: A line from a file that defines a move by an opponent
        followed by a move from a player
    :type input_line: str
    :param expected_score: The score we expect the compute_score method to
        return for each round
    :type expected_score: RoundScore
    :param selection_score_dict: A dictionary that maps a player choice to a
        score associated with that choice
    :type selection_score_dict: dict[PlayerChoice, SelectionScore]
    """
    round_obj = Round.from_string(input_string=input_line, split_string=" ")
    actual_score = round_obj.compute_score(
        selection_score_dict=selection_score_dict)
    assert actual_score == expected_score
