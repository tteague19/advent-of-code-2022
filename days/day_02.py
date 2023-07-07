"""Implements the solution to Day 2 of the Advent of Code 2022."""
from dataclasses import dataclass
from enum import StrEnum


class OpponentChoice(StrEnum):
    """Enumerates the options for a move from the opponent."""
    ROCK = "A"
    PAPER = "B"
    SCISSORS = "C"


class PlayerChoice(StrEnum):
    """Enumerates the options for a move from the player."""
    ROCK = "X"
    PAPER = "Y"
    SCISSORS = "Z"


@dataclass
class Round:
    """Contains the moves from the opponent and player."""
    opponent_choice: OpponentChoice
    player_choice: PlayerChoice

    @classmethod
    def from_string(cls, input_string: str, split_string: str) -> "Round":
        """
        Create an object from a line in an input file of the expected format.

        :param input_string: A line from a file that defines the move an
            opponent makes followed by the :param:`split_string` and then the
            move the player makes
        :type input_string: str
        :param split_string: The string that separates the opponent and player
            moves in the :param:`input_string`
        :type split_string: str
        :return: An object of the class that contains the moves in the
            :param:`input_string`
        :rtype: Round
        """
        moves = input_string.strip().split(split_string)
        opponent_move_idx = list(OpponentChoice).index(moves[0])
        player_move_idx = list(PlayerChoice).index(moves[1])
        return Round(
            opponent_choice=list(OpponentChoice)[opponent_move_idx],
            player_choice=list(PlayerChoice)[player_move_idx],
        )
