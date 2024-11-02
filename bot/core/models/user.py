from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class User(Base):
    tg_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    tg_name: Mapped[str] = mapped_column(nullable=True)
    username: Mapped[str] = mapped_column(unique=True)
    mailing: Mapped[bool] = mapped_column(Boolean(), default=True)
    city: Mapped[str] = mapped_column(String(), nullable=True)
    active: Mapped[bool] = mapped_column(Boolean(), default=True)
