from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import Command
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from states import *
from llm_interaction import get_question_with_answer
from random import choice
import game
import db_interaction
from aiogram import html


introduction_router = Router()
kb_in_game = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Крутить барабан"), KeyboardButton(text="Сказать слово")]], resize_keyboard=True)
kb_new_game = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Новая игра"), KeyboardButton(text="Таблица лидеров")]], resize_keyboard=True)


@introduction_router.message(Command("start"))
async def start_message(message: Message, state: FSMContext) -> None:
    await state.set_state(IntroductionStates.intro_state)
    await message.answer("Привет! Я бот \"Поле чудес\". Приступим к игре?", reply_markup=kb_new_game)


@introduction_router.message(IntroductionStates.intro_state, F.text=="Новая игра")
async def get_new_question(message: Message, state: FSMContext) -> None:
  topics = []
  with open("topics.txt", encoding="utf-8") as topics_file:
     topics = topics_file.readlines()
  topic = choice(topics)  
  question, answer = get_question_with_answer(topic)
  part_of_answer = game.generate_empty_word(answer)
  await state.set_state(GuessingStates.intro_state)
  data = dict()
  data["total_score"] = 0
  data["current_score"] = 0
  data["answer"] = answer
  data["part"] = part_of_answer
  await state.set_data(data=data)
  await message.answer(f"Вопрос по теме \"{topic}\":")
  await message.answer(question)
  await message.answer(f"Слово: {" ".join(list(part_of_answer))}", reply_markup=kb_in_game)


@introduction_router.message(IntroductionStates.intro_state, F.text=="Таблица лидеров")
async def get_statistics(message: Message, state: FSMContext) -> None:
   table = await db_interaction.get_scores()
   if len(table) == 0:
      await message.answer("Еще никто не участвовал в игре. Может, вы будете первым?")
      return
   scores = list()
   for index, (_, username, id, score) in enumerate(table):
      link = f"tg://user?id={id}"
      scores.append(f"{index + 1}.{html.link(username, link)} - {score}")
   new_message = "\n".join(scores)
   await message.answer("Таблица лидеров:")
   await message.answer(new_message, reply_markup=kb_new_game, parse_mode="HTML")
