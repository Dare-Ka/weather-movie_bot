import logging

from core.config import settings

from db.models import db, backup_db
from core.middlewares.middleware import ThrottlingMiddleware
from core.scheduler.settings import set_events
from core.middlewares.apschedulermiddleware import SchedulerMiddleware
from main_menu import router as main_router
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.utils.chat_action import ChatActionMiddleware
from aiogram.fsm.storage.redis import RedisStorage


async def start_bot(bot: Bot):
    await bot.send_message(chat_id=settings.ADMIN_ID, text="Бот запущен!")
    await db.create_table()
    await backup_db.create_table()


async def stop_bot(bot: Bot):
    await bot.send_message(chat_id=settings.ADMIN_ID, text="Бот остановлен!")


async def main():
    bot = Bot(token=settings.TESTBOT_TOKEN)
    storage = RedisStorage.from_url("redis://localhost:6379/0")
    throttling_storage = RedisStorage.from_url("redis://localhost:6379/1")
    scheduler = set_events(bot)
    dp = Dispatcher(storage=storage)
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    dp.update.middleware.register(ThrottlingMiddleware(throttling_storage))
    dp.message.middleware(ChatActionMiddleware())
    dp.update.middleware.register(SchedulerMiddleware(scheduler))
    dp.include_router(main_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s.%(msecs)03d] %(module)s:%(lineno)d %(levelname)s - %(message)s",
    )
    asyncio.run(main())
