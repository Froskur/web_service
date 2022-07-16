from fastapi import FastAPI, Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.db import db_manager
from app.model.user_model import UserInDB, User

# Общие функции, для авторизации и проверки пользователя
#
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")  # use token authentication

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user_from_base = await db_manager.get_user_by_token(token)
    if not user_from_base:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials", headers={"WWW-Authenticate": "Bearer"})

    return User(**user_from_base)


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    # Пока у себя отключил так как не использую, но оставил из гайда для красоты
    # if current_user.disabled:
    #    raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

