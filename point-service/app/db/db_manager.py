from app.model.point_model import PointIn
from app.db.db import points, database
from datetime import datetime


async def add_point(m: PointIn):
    query = points.insert().values(**m.dict())

    return await database.execute(query=query)


async def get_all_points(page_size=None, page_num=None):
    query = points.select()

    if page_size:
        query = query.limit(page_size)

    if page_num:
        query = query.offset(page_num * page_size)

    return await database.fetch_all(query=query)


async def get_point(id):
    query = points.select(points.c.id == id)
    return await database.fetch_one(query=query)


async def delete_point(id: int):
    query = points.delete().where(points.c.id == id)
    return await database.execute(query=query)


async def update_point(id: int, m: PointIn):

    dict_for_update = m.dict()
    dict_for_update["updated_at"] = datetime.now()

    query = (
        points
        .update()
        .where(points.c.id == id)
        .values(**dict_for_update)
    )
    return await database.execute(query=query)
