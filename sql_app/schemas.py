from pydantic import BaseModel

#khai báo schemas item
class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

# khai bao schemas user
class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True
#khia báo schemas email
class Email(BaseModel):
    email: str
    message: str


class Emailusers(Email):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True