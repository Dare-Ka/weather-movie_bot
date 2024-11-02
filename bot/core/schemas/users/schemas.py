from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    tg_id: int
    tg_name: str
    username: str


class UserCreate(UserBase):
    pass


class UserUpdate(UserCreate):
    tg_name: str | None = None
    username: str | None = None
    mailing: bool = True
    city: str | None = None


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
