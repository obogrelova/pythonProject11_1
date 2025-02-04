import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from config import WEATHER, TOKEN
import requests


def get_weather(city):
    api_key = WEATHER
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=ru&appid={api_key}"
    response = requests.get(url)
    weather = response.json()
    if response.status_code != 200:
        return f"Погоду в {city} узнать не получилось. Проверьте название города."
    place = weather['name']
    temperature = weather['main']['temp']
    description = weather['weather'][0]['description']
    return f"Погода в {place}\nТемпература: {temperature}°C\nПогода: {description}"


bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer('Привет! Это бот прогноза погоды. \n\nОтправьте боту название города и он скажет, какая там температура.')

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer('Этот бот умеет выполнять команды:\n/start\n/help\n/weather')

@dp.message(Command('weather'))
async def ask_city(message: Message):
    await message.answer('Пожалуйста, введите название города.')

@dp.message()
async def weather_info(message: Message):
    city = message.text
    await message.answer(get_weather(city))


async def main():
    await dp.start_polling(bot)


if __name__=="__main__":
    asyncio.run(main())