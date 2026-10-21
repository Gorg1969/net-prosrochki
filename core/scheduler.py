# ЗАГЛУШКА
import asyncio
import logging

logger = logging.getLogger(__name__)


async def start_scheduler(bot):
    """Фоновый цикл напоминаний. Пока заглушка — только лог."""
    while True:
        logger.info("[scheduler] stub: проверка сроков (заглушка)")
        # TODO: SELECT из SQLite WHERE days_left IN (7,3,1) AND notified_*=0
        #       → bot.send_message(...) → UPDATE notified_*=1
        await asyncio.sleep(3600 * 6)
