import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.chat_action import ChatActionMiddleware

from bot.core.config import settings
from bot.core.middlewares.apschedulermiddleware import SchedulerMiddleware
from bot.core.middlewares.middleware import ThrottlingMiddleware
from bot.core.models import db_helper
from bot.core.scheduler.settings import set_events
from bot.main_menu import router as main_router


async def start_bot(bot: Bot):
    await bot.send_message(chat_id=settings.bot.admin_id, text="Бот запущен!")


async def stop_bot(bot: Bot):
    await bot.send_message(chat_id=settings.bot.admin_id, text="Бот остановлен!")
    await db_helper.dispose()


async def main():
    bot = Bot(token=settings.bot.token)
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
