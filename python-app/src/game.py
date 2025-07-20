import gamecodes


def check_letter(part: str, full_word: str, letter: str) -> tuple[gamecodes.LetterCodes, str]:
    letter = letter.upper()
    print(letter, full_word)
    if len(letter) > 1:
        return gamecodes.LetterCodes.MORE_ONE_LETTER, part
    if letter in part:
        return gamecodes.LetterCodes.LETTER_ALREADY_IN_WORD, part
    if letter in full_word:
        word_arr = list(part)
        for i in range(len(full_word)):
            if full_word[i] == letter:
                word_arr[i] = letter
        part = "".join(word_arr)
        return gamecodes.LetterCodes.CORRECT_LETTER, part
    return gamecodes.LetterCodes.INCORRECT_LETTER, part


def check_word(word: str, guess: str) ->gamecodes.WordCodes:
    if word.upper() == guess:
        return gamecodes.WordCodes.CORRECT_WORD
    return gamecodes.WordCodes.INCORRECT_WORD


def generate_empty_word(word: str) -> str:
    return "_"*len(word)