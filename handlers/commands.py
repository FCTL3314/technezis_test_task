from aiogram import types
from aiogram.filters import CommandStart

from loader import dp


@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Привет! Отправь мне Excel-файл с сайтами для парсинга.")
