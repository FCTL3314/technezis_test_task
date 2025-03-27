from io import BytesIO

import pandas as pd
from aiogram import types
from pydantic import ValidationError

from db.core import SessionLocal
from db.models import Source
from loader import dp, bot
from schemas import SourceSchema
from services.currency_symbol import CustomCurrencySymbols
from services.parsing import parse_price_by_xpath
from currency_converter import CurrencyConverter


@dp.message(lambda message: message.document)
async def handle_document(message: types.Message):
    document = message.document
    file_id = document.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    file_bytes = await bot.download_file(file_path)
    df = pd.read_excel(BytesIO(file_bytes.read()))

    columns = list(SourceSchema.model_fields.keys())  # noqa

    if not all(col.strip() in columns for col in df.columns):
        await message.answer(f"Файл должен содержать колонки: {", ".join(columns)}.")
        return

    try:
        sources = [SourceSchema(**row.to_dict()) for i, row in df.iterrows()]
    except ValidationError as e:
        await message.answer(
            f"Ошибка при парсинге файла, проверьте что он действительно в нужном формате. {e}"
        )
        return

    with SessionLocal() as session:
        try:
            for source in sources:
                db_source = Source(
                    title=source.title, url=str(source.url), xpath=source.xpath
                )
                session.add(db_source)
            session.commit()
        except Exception as e:
            print(e)
            session.rollback()
            await message.answer("Ошибка при сохранении в базу данных.")
            return

    await message.answer("Файл загружен и сохранен! Начинаю парсинг...")

    message_result = []
    converted_prices = []
    c = CurrencyConverter()

    for i, source in enumerate(sources):
        price = await parse_price_by_xpath(str(source.url), source.xpath)
        message_result.append(f"{i}. {source.title}: {price.amount} {price.currency}")

        currency = CustomCurrencySymbols.get_currency(price.currency)
        if currency == "USD":
            converted_price = float(price.amount)
        else:
            converted_price = c.convert(float(price.amount), currency, "USD")

        converted_prices.append(converted_price)

    avg_price = sum(converted_prices) / len(converted_prices)

    await message.answer(
        f'Результат парсинга:\n{"\n".join(message_result)}.\n\nСредняя цена: {round(avg_price, 2)} $'
    )
