from aiogram.fsm.state import StatesGroup, State


class IntroductionStates(StatesGroup):
    intro_state = State()

class GuessingStates(StatesGroup):
    intro_state = State()
    letter_state = State()
    word_state = State()
