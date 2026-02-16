from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserOut(BaseModel):
    id: int
    email: str
    name: Optional[str] = None
    nickname: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    email: Optional[str] = None
    name: Optional[str] = None
    nickname: Optional[str] = None

    class Config:
        orm_mode = True


class ChangePassword(BaseModel):
    old_password: str
    new_password: str

    class Config:
        orm_mode = True
