# Используемые модели
from pydantic import BaseModel
from typing import Union, Optional, List
from datetime import datetime


class User(BaseModel):
    id: int
    name: Union[str, None] = None
    last_login: Union[datetime, None] = None
    updated_at: Union[datetime, None] = None
    created_at: Union[datetime, None] = None
    #disabled: Union[bool, None] = None


class UserInDB(User):
    hashed_password: Optional[str]
    token: Optional[str]
    last_login: Optional[datetime]
    updated_at: datetime
    created_at: datetime
