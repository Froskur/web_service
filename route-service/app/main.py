from fastapi import FastAPI
from app.router.routes import routes
from app.db.db import database

description = """
API для доступа к маршрутам!

Работает на микро-сервисе. Сделано в качестве **тестового задания**.
"""


app = FastAPI(openapi_url="/api/v1/routes/openapi.json", docs_url="/api/v1/routes/docs",
              title="Routes:API",
              description=description,
              version="1.0.0"
              )


app.include_router(routes, prefix='/api/v1/routes', tags=['routes'])


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()



