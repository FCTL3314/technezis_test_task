import sqlite3
from io import BytesIO

import pandas as pd
from aiogram import types

from loader import settings
from loader import dp, bot
from services.parsing import parse_price


@dp.message(lambda message: message.document)
async def handle_document(message: types.Message):
    document = message.document
    file_id = document.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    file_bytes = await bot.download_file(file_path)
    df = pd.read_excel(BytesIO(file_bytes.read()))

    if not all(col in df.columns for col in ["title", "url", "xpath"]):
        await message.answer("Файл должен содержать колонки: title, url, xpath.")
        return

    with sqlite3.connect(settings.db_engine) as conn:
        df.to_sql("sources", conn, if_exists="append", index=False)

    await message.answer("Файл загружен и сохранен! Начинаю парсинг...")

    results = []
    for _, row in df.iterrows():
        price = await parse_price(row['url'], row['xpath'])
        results.append(f"{row['title']}: {price}")

    await message.answer("\n".join(results))