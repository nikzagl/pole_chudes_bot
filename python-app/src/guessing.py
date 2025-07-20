from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from states import *
from llm_interaction import get_question_with_answer
import game
from random import choice
import db_interaction


guessing_router = Router()
scores = [0, 200, 400, 600, 800, 1000]
kb_in_game = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Крутить барабан"), KeyboardButton(text="Сказать слово")]], resize_keyboard=True)
kb_new_game = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Новая игра"), KeyboardButton(text="Таблица лидеров")]], resize_keyboard=True)


@guessing_router.message(GuessingStates.intro_state, F.text=="Крутить барабан")
async def get_letter(message: Message, state: FSMContext):
    score = choice(scores)
    if score == 0:
        await state.update_data(total_score=0)
        part_of_word = await state.get_value("part")
        await message.answer("На барабане сектор \"Банкрот\". Все ваши очки за текущую игру сгорают")
        await message.answer(f"Слово: {" ".join(list(part_of_word))}", reply_markup=kb_in_game)
        return 
    await state.update_data(current_score=score)
    await message.answer(f"На барабане {score} очков")
    await state.set_state(GuessingStates.letter_state)
    await message.answer("Введите букву:", reply_markup = ReplyKeyboardRemove())


@guessing_router.message(GuessingStates.intro_state, F.text=="Сказать слово")
async def get_letter(message: Message, state: FSMContext):
    await state.set_state(GuessingStates.word_state)
    await message.answer("Введите слово целиком:", reply_markup=ReplyKeyboardRemove())


@guessing_router.message(GuessingStates.letter_state)
async def check_letter(message: Message, state: FSMContext):
    letter = message.text
    data = await state.get_data()
    part_of_word = data["part"]
    word = data["answer"]
    current_score = data["current_score"]
    prev_score = data["total_score"]
    result, part_of_word = game.check_letter(part_of_word, word, letter)
    if word == part_of_word:
        await state.update_data(total_score=prev_score + current_score)
        await state.set_state(IntroductionStates.intro_state)
        await message.answer(f"Вы правильно отгадали слово {word}", reply_markup=kb_new_game)
        await message.answer(f"Вы получили {prev_score + current_score} очков за игру!")
        await db_interaction.update_user(message.from_user.full_name, str(message.from_user.id), prev_score+current_score)
        return
    
    await state.update_data(part = part_of_word)
    if result == game.gamecodes.LetterCodes.CORRECT_LETTER:
        await message.answer("Такая буква есть в этом слове!")
        await state.update_data(total_score=current_score+prev_score)
    elif result == game.gamecodes.LetterCodes.INCORRECT_LETTER:
        await message.answer("Увы, но такой буквы в слове нет!")
    elif result == game.gamecodes.LetterCodes.LETTER_ALREADY_IN_WORD:
        await message.answer("Вы уже называли эту букву!")
    else:
        await message.answer("Названа не буква!")
    await state.set_state(GuessingStates.intro_state)
    await message.answer(f"Слово: {" ".join(list(part_of_word))}", reply_markup=kb_in_game)


@guessing_router.message(GuessingStates.word_state)
async def check_word(message: Message, state: FSMContext):
    guess = message.text
    data = await state.get_data()
    prev_score = data["total_score"]
    word = data["answer"]
    result = game.check_word(guess, word)
    if result == game.gamecodes.WordCodes.CORRECT_WORD:
        await state.set_state(IntroductionStates.intro_state)
        await message.answer(f"Вы правильно отгадали слово {word}!")
        await message.answer("+400 очков за правильно угаданное слово")
        new_score = prev_score+400
        await state.update_data(total_score=new_score)
        await message.answer(f"Вы получили {new_score} за игру!", reply_markup=kb_new_game)
        await db_interaction.update_user(message.from_user.full_name, str(message.from_user.id), new_score)
    else:
        await message.answer(f"Это не то слово!")
        await state.update_data(total_score=0)
        await message.answer(f"Вы получили 0 очков за игру", reply_markup=kb_new_game)
        await state.set_state(IntroductionStates.intro_state)
        await db_interaction.update_user(message.from_user.full_name, str(message.from_user.id), 0)
        


