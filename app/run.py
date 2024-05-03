import asyncio
from aiogram import Bot, Dispatcher

from config import TG_TOKEN
from handlers import router


bot = Bot(token=TG_TOKEN)
dp = Dispatcher()


async def main() -> None:
    """
    Program's entry point.
    """

    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
