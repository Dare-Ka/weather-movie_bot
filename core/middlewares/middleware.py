from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Update

from core.models import db_helper
from database.users.crud import update_user, get_user
from database.users.schemas import UserUpdate


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, storage: RedisStorage):
        self.storage = storage

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        session = await db_helper.get_scoped_session()
        if event.message:
            found_user = await get_user(
                session=session, tg_id=event.message.from_user.id
            )
            user_update = UserUpdate(
                tg_id=event.message.from_user.id,
                tg_name=event.message.from_user.first_name,
                username=event.message.from_user.username,
            )
            await update_user(session=session, user_update=user_update, user=found_user)
            user = f"user{event.message.from_user.id}"
            check_user = await self.storage.redis.get(name=user)
            if check_user:
                if int(check_user.decode()) == 1:
                    await self.storage.redis.set(name=user, value=0, ex=1)
                    return await event.message.answer(
                        "Замечена подозрительная активность! Подожди немного"
                    )
                return
            await self.storage.redis.set(name=user, value=1, ex=1)

            return await handler(event, data)
        if event.callback_query:
            found_user = await get_user(
                session=session, tg_id=event.callback_query.from_user.id
            )
            user_update = UserUpdate(
                tg_id=event.callback_query.from_user.id,
                tg_name=event.callback_query.from_user.first_name,
                username=event.callback_query.from_user.username,
            )
            await update_user(session=session, user_update=user_update, user=found_user)
            user = f"user{event.callback_query.from_user.id}"
            check_user = await self.storage.redis.get(name=user)
            if check_user:
                if int(check_user.decode()) == 1:
                    await self.storage.redis.set(name=user, value=0, ex=1)
                    return await event.callback_query.message.answer(
                        "Замечена подозрительная активность! Подожди немного"
                    )
                return
            await self.storage.redis.set(name=user, value=1, ex=1)

            return await handler(event, data)
