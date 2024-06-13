from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import TelegramObject, Message, CallbackQuery

from db.models import db, backup_db


class ThrottlingCallBackMiddleware(BaseMiddleware):
    def __init__(self, storage: RedisStorage):
        self.storage = storage

    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: CallbackQuery,
                       data: Dict[str, Any]) -> Any:
        await db.update_user(
            tg_id=event.from_user.id,
            tg_name=event.from_user.first_name,
            username=event.from_user.username
        )
        await backup_db.update_user(
            tg_id=event.from_user.id,
            tg_name=event.from_user.first_name,
            username=event.from_user.username
        )
        user = f'user{event.from_user.id}'
        check_user = await self.storage.redis.get(name=user)
        if check_user:
            if int(check_user.decode()) == 1:
                await self.storage.redis.set(name=user, value=0, ex=2)
                return await event.message.answer('Замечена подозрительная активность! Подожди немного')
            return
        await self.storage.redis.set(name=user, value=1, ex=2)

        return await handler(event, data)


class ThrottlingMessageMiddleware(BaseMiddleware):
    def __init__(self, storage: RedisStorage):
        self.storage = storage

    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any]) -> Any:
        await db.update_user(
            tg_id=event.from_user.id,
            tg_name=event.from_user.first_name,
            username=event.from_user.username
        )
        await backup_db.update_user(
            tg_id=event.from_user.id,
            tg_name=event.from_user.first_name,
            username=event.from_user.username
        )
        user = f'user{event.from_user.id}'
        check_user = await self.storage.redis.get(name=user)
        if check_user:
            if int(check_user.decode()) == 1:
                await self.storage.redis.set(name=user, value=0, ex=1)
                return await event.answer('Замечена подозрительная активность! Подожди немного')
            return
        await self.storage.redis.set(name=user, value=1, ex=1)

        return await handler(event, data)

