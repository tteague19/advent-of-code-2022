"""Implements the solution to Day 2 of the Advent of Code 2022."""
from dataclasses import dataclass
from enum import StrEnum, IntEnum
from pathlib import Path
from typing import Sequence

RoundScore = int
SelectionScore = int


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


class RoundOutcome(IntEnum):
    """Enumerates the possible outcomes of a round and the outcome scores."""
    LOSS = 0
    DRAW = 3
    WIN = 6


PLAYER_SELECTION_TO_SCORE_DICT: dict[PlayerChoice, SelectionScore] = {
    PlayerChoice.ROCK: 1,
    PlayerChoice.PAPER: 2,
    PlayerChoice.SCISSORS: 3,
}


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

    def determine_outcome(self) -> RoundOutcome:
        """
        Determine the outcome of a game of Rock Paper Scissors for the player.

        :return: The outcome of the round the object represents
        :rtype: RoundOutcome
        """
        if self.player_choice.name == self.opponent_choice.name:
            return RoundOutcome.DRAW

        player_wins = any(
            [
                all(
                    [
                        self.player_choice == PlayerChoice.ROCK,
                        self.opponent_choice == OpponentChoice.SCISSORS
                    ]
                ),
                all(
                    [
                        self.player_choice == PlayerChoice.PAPER,
                        self.opponent_choice == OpponentChoice.ROCK
                    ]
                ),
                all(
                    [
                        self.player_choice == PlayerChoice.SCISSORS,
                        self.opponent_choice == OpponentChoice.PAPER
                    ]
                )
            ]
        )

        if player_wins:
            return RoundOutcome.WIN

        # If the outcome is not a draw or a scenario where the player wins,
        # the player must have lost.
        return RoundOutcome.LOSS

    def compute_score(
            self,
            selection_score_dict: dict[PlayerChoice, SelectionScore],
    ) -> RoundScore:
        """
        Compute the total score of the round represented by the object

        :param selection_score_dict: A dictionary that maps a player choice to
            a score associated with that choice
        :type selection_score_dict: dict[PlayerChoice, SelectionScore]
        :return: The total score of the round with respect to the player
        :rtype: RoundScore
        """
        outcome = self.determine_outcome()
        selection_score = selection_score_dict[self.player_choice]
        return outcome.value + selection_score


@dataclass
class Game:
    """Models a series of rounds of a game of Rock Paper Scissors"""
    rounds: Sequence[Round]

    @classmethod
    def from_file(cls, file_path: Path, split_string: str) -> "Game":
        """
        Construct a Game object from the contents of a structured input file.

        :param file_path: The path to a file where each line defines the move
            an opponent makes followed by the :param:`split_string` and then
            the move the player makes
        :type file_path: Path
        :param split_string: The string that separates the opponent and player
            moves in each line of the file at :param:`file_path`
        :type split_string: str
        :return: An object of the Game class whose rounds attribute is
            constructed from the file at :param:`file_path`
        :rtype: Game
        """
        with file_path.open(mode="r") as f:
            rounds = [
                Round.from_string(input_string=line, split_string=split_string)
                for line in f.readlines()
            ]
        return Game(rounds=rounds)
