from aiogram import Bot, Dispatcher, dispatcher, types
from aiogram.filters import CommandStart
import asyncio
import os
from config import config

bot = Bot(config["TOKEN"])

dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(msg: types.Message):
    await msg.answer("Привет")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
