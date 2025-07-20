from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.memory import MemoryStorage
import logging
from dotenv import load_dotenv
import os
import asyncio
from introduction import introduction_router
from guessing import guessing_router


logging.basicConfig(level = logging.INFO)


TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")


bot = Bot(token = TELEGRAM_TOKEN)
storage = RedisStorage.from_url("redis://redis:6379/0")
dp = Dispatcher(storage=storage)
dp.include_router(introduction_router)
dp.include_router(guessing_router)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
