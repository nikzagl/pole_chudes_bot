from enum import Enum


class LetterCodes(Enum):
    CORRECT_LETTER = 0
    INCORRECT_LETTER = 1
    LETTER_ALREADY_IN_WORD = 2
    MORE_ONE_LETTER = 3


class WordCodes(Enum):
    CORRECT_WORD = 0
    INCORRECT_WORD = 1
