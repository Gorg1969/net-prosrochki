import asyncio
import logging
import os

from dotenv import load_dotenv
from aiomax2 import Bot, Dispatcher

from .handlers import router
from core.scheduler import start_scheduler

load_dotenv()
logger = logging.getLogger(__name__)


async def _main():
    token = os.environ.get("MAX_BOT_TOKEN")
    if not token:
        raise RuntimeError("Не задан MAX_BOT_TOKEN (см. .env.example)")

    bot = Bot(token)
    dp = Dispatcher()
    dp.include_router(router)

    # Фоновая задача напоминаний (пока заглушка)
    scheduler_task = asyncio.create_task(start_scheduler(bot))

    logger.info("Бот запущен")
    try:
        await dp.start_polling(bot)
    finally:
        scheduler_task.cancel()
        await bot.close()
        await dp.close()


def run():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    asyncio.run(_main())
