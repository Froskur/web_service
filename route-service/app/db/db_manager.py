from app.model.route_model import RouteIn
from app.db.db import routes, points, routes_points, database
from sqlalchemy.sql import select


async def add_route(m: RouteIn):
    query = routes.insert().values(**m.dict(exclude={'points'}))
    route_id = await database.execute(query=query)

    # Подготовим данные для крос таблицы
    points_in_route = []
    for p in m.points:
        points_in_route.append({
            'route_id': route_id,
            'point_id': p.id,
            'ord': p.ord
        })

    # Теперь просто пуляем в таблицу эти данные
    await database.execute_many(routes_points.insert(), points_in_route)

    return route_id


async def get_all_routes(page_size=None, page_num=None):
    query = routes.select()

    if page_size:
        query = query.limit(page_size)

    if page_num:
        query = query.offset(page_num * page_size)

    return await database.fetch_all(query=query)


async def get_route(id: int):
    query = routes.select(routes.c.id == id)
    return await database.fetch_one(query=query)


async def get_points_for_route(id: int):

    query = select([routes_points.c.ord, points]).\
                where(routes_points.c.route_id == id).\
                select_from(routes_points.join(points)).\
                order_by(routes_points.c.ord)

    return await database.fetch_all(query=query)
