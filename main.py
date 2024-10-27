import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.chat_action import ChatActionMiddleware

from core.config import settings
from core.middlewares.apschedulermiddleware import SchedulerMiddleware
from core.middlewares.middleware import ThrottlingMiddleware
from core.models import Base, db_helper
from core.scheduler.settings import set_events
from main_menu import router as main_router


async def start_bot(bot: Bot):
    await bot.send_message(chat_id=settings.ADMIN_ID, text="Бот запущен!")
    async with db_helper.engin.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def stop_bot(bot: Bot):
    await bot.send_message(chat_id=settings.ADMIN_ID, text="Бот остановлен!")


async def main():
    bot = Bot(token=settings.TESTS_BOT_TOKEN)
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
