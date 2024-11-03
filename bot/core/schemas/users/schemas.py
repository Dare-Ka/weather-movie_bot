from pydantic import BaseModel


class UserBase(BaseModel):
    tg_id: int
    tg_name: str | None
    username: str | None


class UserCreate(UserBase):
    pass


class UserUpdate(UserCreate):
    tg_name: str | None = None
    username: str | None = None
    mailing: bool | None = None
    city: str | None = None
    active: bool | None = None
