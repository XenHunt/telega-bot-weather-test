from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart
import asyncio

import logging

import requests
from config import config
from models import manualAdd, findLastCity

bot = Bot(config["BOT_TOKEN"])

dp = Dispatcher()


@dp.message(Command("weather"))
async def get_weather(msg: types.Message):
    text = msg.text
    user = msg.from_user
    if user is None:
        await msg.answer("Ты не пользователь")
        manualAdd(-1, text if text is not None else "Error", "Ты не пользователь")
        return

    userid = user.id
    try:
        last_city = findLastCity(userid)
    except Exception as e:
        print(e)
        last_city = None
    if (
        text is None
        or len(text.split()) == 1
        and last_city is None
        or len(text.split()) > 2
    ):
        await msg.answer("Не коректная команда (\\weather <название города>)")
        manualAdd(
            user.id,
            text if text is not None else "Error",
            "Не коректная команда (\\weather <название города>)",
        )
        return

    city = text.split()[1] if len(text.split()) == 2 else last_city
    url = f"https://ru.api.openweathermap.org/data/2.5/weather?q={city}&appid={config['WEATHER_TOKEN']}&units=metric&lang=ru"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        weather, temp, wind = data["weather"][0], data["main"], data["wind"]

        ans = f"На данный момент погода в городе {city}:\nТемпература🌡️ {temp['temp']}°C\nОщущается🧥 как {temp['feels_like']}°C\nПогода☁️ - {weather['main']}, {weather['description']}\nВлажность💧 - {temp['humidity']}\nСкорость ветра🌬️ - {wind['speed']} м/с"
        await msg.answer(ans)
    else:
        ans = "Incorrect city or service (openweather) is down."
        await msg.answer(ans)

    manualAdd(userid, text, ans)


@dp.message(CommandStart())
async def cmd_start(msg: types.Message):
    user = msg.from_user
    if user is None:
        await msg.answer("Ты не пользователь")
        manualAdd(-1, "/start", "Ты не пользователь")
        return
    userid = user.id
    ans = "Вы запустили бота BobrAI для выяснеиея погоды\nОсновная комманда: \\weather <название города>; для выяснениея нынешней погоды в городе"
    manualAdd(userid, "/start", ans)
    await msg.answer(ans)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
