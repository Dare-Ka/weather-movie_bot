from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from bot.core.models import User
from core.schemas.users.schemas import UserCreate, UserUpdate


async def get_users(session: AsyncSession) -> list[User]:
    statement = select(User).order_by(User.id)
    result: Result = await session.execute(statement)
    users = result.scalars().all()
    return users


async def get_mailing_users(session: AsyncSession) -> list[User]:
    statement = select(User).order_by(User.id).where(User.mailing == True)
    result: Result = await session.execute(statement)
    users = result.scalars().all()
    return users


async def get_user(session: AsyncSession, tg_id: int) -> User | None:
    statement = select(User).where(User.tg_id == tg_id)
    result: Result = await session.execute(statement)
    user_id = result.scalar_one().id
    user = await session.get(User, user_id)
    return user


async def add_user(session: AsyncSession, user_in: UserCreate) -> User:
    user = User(**user_in.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def update_user(
    session: AsyncSession,
    user: User,
    user_update: UserUpdate,
) -> User:
    for name, value in user_update.model_dump(exclude_unset=True).items():
        setattr(user, name, value)
    await session.commit()
    return user


async def delete_user(session: AsyncSession, user: User) -> None:
    await session.delete(user)
    await session.commit()
