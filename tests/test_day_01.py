"""Tests the solution for Day 1 of the Advent of Code."""
from pathlib import Path

import pytest

from days.day_01 import parse_input_file, SnackCalories, ElfName, \
    identify_elf_with_highest_calories, create_elf_name

SIMPLE_INPUT_FILE_PATH = Path(__file__).parent.joinpath(
    "input-files", "day-01-simple.txt")


@pytest.mark.parametrize(
    "file_path,expected_output",
    [
        [
            SIMPLE_INPUT_FILE_PATH,
            {
                create_elf_name(idx=idx, padding_amount=2): calorie_list
                for idx, calorie_list in enumerate(
                    [
                        [1000, 2000, 3000],
                        [4000],
                        [5000, 6000],
                        [7000, 8000, 9000],
                        [10000],
                    ],
                    start=1,
                )
            },
        ]
    ]
)
def test_parse_input_file(
        file_path: Path,
        expected_output: dict[ElfName, list[SnackCalories]],
) -> None:
    actual_output = parse_input_file(file_path=file_path, line_delimiter="\n")
    assert expected_output == actual_output


@pytest.mark.parametrize(
    "elf_to_snacks_dict,expected_output",
    [
        [
            parse_input_file(
                file_path=SIMPLE_INPUT_FILE_PATH, line_delimiter="\n"),
            (create_elf_name(idx=4, padding_amount=2), 24000)
        ],
    ]
)
def test_identify_elf_with_highest_calories(
        elf_to_snacks_dict: dict[ElfName, list[SnackCalories]],
        expected_output: tuple[ElfName, SnackCalories],
) -> None:
    actual_output = identify_elf_with_highest_calories(
        elf_to_snacks_dict=elf_to_snacks_dict)
    assert expected_output == actual_output
