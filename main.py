import asyncio

from handlers import register_handlers
from loader import dp, bot


async def main() -> None:
    await register_handlers()
    print("Start polling...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
