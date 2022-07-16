from fastapi import FastAPI
from app.router.points import points
from app.db.db import metadata, database, engine

metadata.create_all(engine)

description = """
API для доступа к навигационным точкам!

Работает на микро-сервисе. Сделано в качестве **тестового задания**.
"""

tags_metadata = [
    {
        "name": "points",
        "description": "Доступные методы API для взаимодействия навигационными точками",
    },
]


app = FastAPI(openapi_url="/api/v1/points/openapi.json", docs_url="/api/v1/points/docs",
              title="Points:API",
              description=description,
              version="1.0.0",
              tags_metadata=tags_metadata
              )


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(points, prefix='/api/v1/points', tags=['points'])
