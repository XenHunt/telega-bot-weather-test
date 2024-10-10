from aiogram import Bot, Dispatcher, dispatcher, types
from aiogram.filters import Command, CommandStart
import asyncio
import os

import logging

import requests
from config import config

bot = Bot(config["TOKEN"])

dp = Dispatcher()


@dp.message(Command("weather"))
async def get_weather(msg: types.Message):
    text = msg.text
    if text is None or len(text.split()) != 2:
        await msg.answer("Не коректная команда (\\weather <название города>)")
        return
    city = text.split()[1]
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={config['WEATHER_TOKEN']}&units=metric&lang=ru"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        weather, temp, wind = data["weather"], data["main"], data["wind"]

        ans = f"На данный момент погода в городе {city}:\nТемпература🌡️ - {temp['temp']}°C\nОщущается как {temp['feels_like']}°C\nПогода☁️ - {weather['main']}, {weather['description']}\nВлажность💧 - {temp['humidity']}\nСкорость ветра🌬️ - {wind['speed']}"
        await msg.answer(ans)
    else:
        await msg.answer("Incorrect city or service is down.")


@dp.message(CommandStart())
async def cmd_start(msg: types.Message):
    await msg.answer("Привет")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
