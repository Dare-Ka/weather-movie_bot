from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
)

from core.config import db_settings


class DatabaseHelper:
    def __init__(self, url: str, echo: bool):
        self.engin = create_async_engine(
            url=url,
            echo=echo,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engin,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def get_scoped_session(self) -> AsyncSession:
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    # async def session_dependency(self) -> AsyncSession:
    #     async with self.session_factory() as session:
    #         yield session
    #         await session.close()
    #
    # async def scoped_session_dependency(self) -> AsyncSession:
    #     session = self.get_scoped_session()
    #     yield session
    #     await session.close()


db_helper = DatabaseHelper(
    url=db_settings.db_url,
    echo=db_settings.db_echo,
)
