"""Implements the solution of Day 1 of the Advent of Code."""
from functools import partial
from pathlib import Path
from typing import Sequence

ElfName = str
SnackCalories = int

MIN_PADDING_AMOUNT = 2


def create_elf_name(idx: int, padding_amount: int) -> ElfName:
    """
    Create the name to use for each elf in a standard format.

    :param idx: The index of the elf in the input file
    :type idx: int
    :param padding_amount: The number of leading zeros to use in the name of
        the elf
    :type padding_amount: int
    :return: A name to use for the elf at index :param:`idx`
    :rtype: ElfName

    >>> create_elf_name(idx=10, padding_amount=3)
    'elf-010'
    >>> create_elf_name(idx=19, padding_amount=10)
    'elf-0000000019'
    """
    return f"elf-{idx:>0{padding_amount}}"


def clean_string_per_elf(
        calorie_string: str, delimiter: str) -> list[SnackCalories]:
    """
    Convert a string of delimited sub-strings to a list of calories values.

    :param calorie_string: A string that we assume contains a list of numeric
        values separated by :param:`delimiter`
    :type calorie_string: str
    :param delimiter: A string we assume separates the calorie value of each
        snack in :param:`calorie_string`
    :type delimiter: str
    :return: The input :param:`calorie_string` as a
    :rtype: list[SnackCalories]
    :raises ValueError: We raise a value error if we are unable to convert one
        of the calorie values to a numeric value

    >>> clean_string_per_elf('10000 2000 3000', ' ')
    [10000, 2000, 3000]
    >>> clean_string_per_elf('  10000#2000#3000 ', '#')
    [10000, 2000, 3000]
    """
    try:
        return [
            int(calorie_string)
            for calorie_string
            in calorie_string.strip().split(delimiter)
        ]
    except ValueError:
        print(
            "Please provide a file with appropriate values for calorie counts")


def parse_input_file(
        file_path: Path,
        line_delimiter: str,
) -> dict[ElfName, list[SnackCalories]]:
    """
    Read an input text file and parse the caloric content of each elf's snacks.

    :param file_path: The path to the input text file
    :type file_path: Path
    :param line_delimiter: A string that separates each line in the file at
        :param:`file_path` and that we assume is the entirety of blank lines
        that separate each elf's snacks caloric contents
    :type line_delimiter: str
    :return: A map from each elf to the calorie values of each snack the elf
        packed
    :rtype: dict[ElfName, list[SnackCalories]]
    """
    with file_path.open(mode="r") as f:
        file_contents = f.read()

    list_of_list_of_calories_per_elf = list(
        map(
            lambda calorie_string: clean_string_per_elf(
                calorie_string=calorie_string,
                delimiter=line_delimiter),
            file_contents.split(f"{line_delimiter}{line_delimiter}")
        )
    )

    num_elves = len(list_of_list_of_calories_per_elf)
    elf_name_creation_func = partial(
        create_elf_name,
        padding_amount=max(len(str(num_elves)) + 1, MIN_PADDING_AMOUNT),
    )
    return {
        elf_name_creation_func(idx): calorie_int_list
        for idx, calorie_int_list in enumerate(
            list_of_list_of_calories_per_elf, start=1)
    }


def identify_elf_with_highest_calories(
        elf_to_snacks_dict: dict[ElfName, Sequence[SnackCalories]],
) -> tuple[ElfName, SnackCalories]:
    """
    Find the elf with the highest number of total calories worth of snacks.

    :param elf_to_snacks_dict: A dictionary that maps the names of elves to the
        calorie amount of each snack it packed
    :type elf_to_snacks_dict: dict[ElfName, Sequence[SnackCalories]]
    :return: A tuple containing the name of the elf with the highest total
        calories across all its snacks and the total number of calories across
        its snacks
    :rtype: tuple[ElfName, SnackCalories]
    """
    elf, snacks = max(
        elf_to_snacks_dict.items(), key=lambda item: sum(item[1]))

    return elf, sum(snacks)
