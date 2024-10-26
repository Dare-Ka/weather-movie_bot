from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Update

from db.models import db, backup_db


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, storage: RedisStorage):
        self.storage = storage

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        if event.message:
            await db.update_user(
                tg_id=event.message.from_user.id,
                tg_name=event.message.from_user.first_name,
                username=event.message.from_user.username,
            )
            await backup_db.update_user(
                tg_id=event.message.from_user.id,
                tg_name=event.message.from_user.first_name,
                username=event.message.from_user.username,
            )
            user = f"user{event.message.from_user.id}"
            check_user = await self.storage.redis.get(name=user)
            if check_user:
                if int(check_user.decode()) == 1:
                    await self.storage.redis.set(name=user, value=0, ex=2)
                    return await event.message.answer(
                        "Замечена подозрительная активность! Подожди немного"
                    )
                return
            await self.storage.redis.set(name=user, value=1, ex=2)

            return await handler(event, data)
        if event.callback_query:
            await db.update_user(
                tg_id=event.callback_query.from_user.id,
                tg_name=event.callback_query.from_user.first_name,
                username=event.callback_query.from_user.username,
            )
            await backup_db.update_user(
                tg_id=event.callback_query.from_user.id,
                tg_name=event.callback_query.from_user.first_name,
                username=event.callback_query.from_user.username,
            )
            user = f"user{event.callback_query.from_user.id}"
            check_user = await self.storage.redis.get(name=user)
            if check_user:
                if int(check_user.decode()) == 1:
                    await self.storage.redis.set(name=user, value=0, ex=2)
                    return await event.callback_query.message.answer(
                        "Замечена подозрительная активность! Подожди немного"
                    )
                return
            await self.storage.redis.set(name=user, value=1, ex=2)

            return await handler(event, data)
