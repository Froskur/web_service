from fastapi import FastAPI, Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from passlib.context import CryptContext

from app.db.db import metadata, database, engine

# Роутеры по API микро-сервисов
from app.router.points import points
from app.router.routes import routes
from app.router.reports import reports

from app.db import db_manager
from app.model.user_model import UserInDB, User

from app.util import auth

metadata.create_all(engine)

description = """
Web-сервис для работы с маршрутами

В работе использует три микро сервиса, и одну общую базу данных. Этот сервис агрегирует и выпускает наружу некоторые
из методов API которые доступны у микро-сервисов.      
"""

tags_metadata = [
    {
        "name": "routes",
        "description": "Методы для взаимодействия с маршрутами",
    },
    {
        "name": "points",
        "description": "Методы для для работы с точками маршрутов",
    },
    {
        "name": "reports",
        "description": "Возможные отчеты",
    },

]


app = FastAPI(openapi_url="/api/v1/openapi.json", docs_url="/api/v1/docs",
              title="Gate:API",
              description=description,
              version="1.0.0",
              tags_metadata=tags_metadata
              )

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")  # use token authentication

"""
# Общие функции, для авторизации и проверки пользователя
#
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
"""


# Общие вещи связанные с авторизацией
@app.post("/token",)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_from_base = await db_manager.get_user_by_name(form_data.username)
    if not user_from_base:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    user_from_base = UserInDB(**user_from_base)
    if not(pwd_context.verify(form_data.password, user_from_base.hashed_password)):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    await db_manager.update_last_login(user_from_base)
    return {"access_token": user_from_base.token, "token_type": "bearer", "client_id": user_from_base.id}


@app.get("/me")
async def read_users_me(current_user: User = Depends(auth.get_current_active_user)):
    return current_user

# Подключаем роутинг дополнительных путей, и они у нас все будут требовать авторизацию
authenticated_router = APIRouter(dependencies=[Depends(auth.get_current_active_user)])
authenticated_router.include_router(points, prefix='/api/v1/points', tags=['points'])
authenticated_router.include_router(routes, prefix='/api/v1/routes', tags=['routes'])
authenticated_router.include_router(reports, prefix='/api/v1/reports', tags=['reports'])

app.include_router(authenticated_router)

#
@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()




# This is encrypted in the database
#api_keys = [
#    "akljnv13bvi2vfo0b0bw"
#]

#def api_key_auth(api_key: str = Depends(oauth2_scheme)):
#    if api_key not in api_keys:
#        raise HTTPException(status_code=401, detail="Forbidden")
#
#    user_id = 1
#    return user_id



"""
@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}
"""


@app.get("/items")
async def read_items():
    return {"token": "yes"}
