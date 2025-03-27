from aiogram import Bot, Dispatcher

from config import Settings

settings = Settings()
bot = Bot(token=settings.token)
dp = Dispatcher()
