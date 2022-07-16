from fastapi import FastAPI
from app.router.reports import reports
from app.db.db import metadata, database, engine

metadata.create_all(engine)

description = """
API для доступа к отчетам!

Один отчёт всего тут пока
"""


app = FastAPI(openapi_url="/api/v1/reports/openapi.json", docs_url="/api/v1/reports/docs",
              title="Reports:API",
              description=description,
              version="1.0.0"
              )


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(reports, prefix='/api/v1/reports', tags=['reports'])
