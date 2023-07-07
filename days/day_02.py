"""Implements the solution to Day 2 of the Advent of Code 2022."""
from dataclasses import dataclass
from enum import StrEnum, IntEnum
from pathlib import Path
from typing import Sequence

GameScore = int
RoundScore = int
SelectionScore = int


class ChallengePart(IntEnum):
    """Enumerate which part of the challenge we are in."""
    PART_1 = 1
    PART_2 = 2


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


class PlayerStrategy(StrEnum):
    """Enumerates the strategy the player follows per Part 2 of the puzzle."""
    LOSE = "X"
    DRAW = "Y"
    WIN = "Z"


OPPONENT_MOVE_STRATEGY_TO_PLAYER_MOVE_DICT = {
    (OpponentChoice.ROCK, PlayerStrategy.DRAW): PlayerChoice.ROCK,
    (OpponentChoice.PAPER, PlayerStrategy.DRAW): PlayerChoice.PAPER,
    (OpponentChoice.SCISSORS, PlayerStrategy.DRAW): PlayerChoice.SCISSORS,
    (OpponentChoice.ROCK, PlayerStrategy.WIN): PlayerChoice.PAPER,
    (OpponentChoice.PAPER, PlayerStrategy.WIN): PlayerChoice.SCISSORS,
    (OpponentChoice.SCISSORS, PlayerStrategy.WIN): PlayerChoice.ROCK,
    (OpponentChoice.ROCK, PlayerStrategy.LOSE): PlayerChoice.SCISSORS,
    (OpponentChoice.PAPER, PlayerStrategy.LOSE): PlayerChoice.ROCK,
    (OpponentChoice.SCISSORS, PlayerStrategy.LOSE): PlayerChoice.PAPER,
}


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

    @classmethod
    def from_string_part_two(
            cls, input_string: str, split_string: str) -> "Round":
        """
        Create an object from a line in an input file of the expected format.

        This method adapts the code for the second part of the challenge. We
        learn that the second column of values is not the move the player
        makes but, instead, is the outcome the player should create.

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
        content = input_string.strip().split(split_string)
        opponent_move_idx = list(OpponentChoice).index(content[0])
        opponent_choice = list(OpponentChoice)[opponent_move_idx]

        player_strategy_idx = list(PlayerStrategy).index(content[1])
        player_strategy = list(PlayerStrategy)[player_strategy_idx]
        player_choice = cls.determine_player_choice(
            opponent_choice=opponent_choice,
            player_strategy=player_strategy,
        )
        return Round(
            opponent_choice=opponent_choice, player_choice=player_choice)

    @classmethod
    def determine_player_choice(
            cls,
            opponent_choice: OpponentChoice,
            player_strategy: PlayerStrategy,
    ) -> PlayerChoice:
        """
        Determine the move the player makes given a strategy and opponent.

        In Part 2 of the challenge, we are given the move the opponent makes
        and the outcome the player wants to achieve. This method identifies the
        move the player should make given the opponent's move and the outcome
        the player desires.

        :param opponent_choice: The move the opponent makes
        :type opponent_choice: OpponentChoice
        :param player_strategy: The outcome the player wants to achieve
        :type player_strategy: PlayerStrategy
        :return: The move the player should make given the desired
            :param:`PlayerStrategy` and the opponent's move
            :param:`opponent_choice`
        :rtype: PlayerChoice
        """
        key = (opponent_choice, player_strategy)
        return OPPONENT_MOVE_STRATEGY_TO_PLAYER_MOVE_DICT[key]

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
    def from_file(
            cls,
            file_path: Path,
            split_string: str,
            challenge_part: ChallengePart,
    ) -> "Game":
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
        :param challenge_part: A flag to determine which part of the challenge
            to assume, which influences the interpretation of the data to
            construct each round object
        :rtype: Game
        """
        if challenge_part == ChallengePart.PART_1:
            with file_path.open(mode="r") as f:
                rounds = [
                    Round.from_string(
                        input_string=line, split_string=split_string)
                    for line in f.readlines()
                ]
        else:
            with file_path.open(mode="r") as f:
                rounds = [
                    Round.from_string_part_two(
                        input_string=line, split_string=split_string)
                    for line in f.readlines()
                ]

        return Game(rounds=rounds)

    def compute_score(
            self,
            selection_score_dict: dict[PlayerChoice, SelectionScore],
    ) -> GameScore:
        """
        Compute the total score based on the individual round scores.

        :param selection_score_dict: A dictionary that maps a player choice in
            a round to a score associated with that choice
        :type selection_score_dict: dict[PlayerChoice, SelectionScore]
        :return: The total score for the game, which is the sum of the scores
            for each round of the game
        :rtype: GameScore
        """
        round_scores = [
            round_obj.compute_score(selection_score_dict=selection_score_dict)
            for round_obj in self.rounds
        ]
        return sum(round_scores)
