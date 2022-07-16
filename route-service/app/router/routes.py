from typing import List
from fastapi import APIRouter, HTTPException

from app.model.route_model import RouteIn, RouteOut, PointOutInRoute, PointNew
from app.db import db_manager
from app.service.service import points_add
from app.model.track import get_optimal_track_for_route

routes = APIRouter()


@routes.post('/', response_model=RouteOut, status_code=201, description="Создает новый маршрут с набором точек")
async def create_route(m: RouteIn):

    points_dict = [dict(x) for x in m.points]
    # raise HTTPException(status_code=422, detail=f"Тестовая выдача: {points_dict}")

    r = points_add(points_dict)
    if r.status_code != 201:
        raise HTTPException(status_code=422, detail=f"Errors added new points: {r.json()}")

    m.points = []
    for index, p in enumerate(r.json()):
        p["ord"] = (index+1)*10
        m.points.append(PointOutInRoute(**p))

    # Сначала маршрут сам справиться и добавит точки
    route_id = await db_manager.add_route(m)

    return await get_route(route_id)


@routes.post('/optimal', response_model=List[PointNew],
             description="Считаем оптимальный маршрут для набора точек. Выдача будет содержать те же точки, но в другом порядке.")
async def optimal_route(p: List[PointNew]):
    if not(2 <= len(p) <= 10):
        raise HTTPException(status_code=406, detail=f"Count point needle between 2 and 10")

    return await get_optimal_track_for_route(p)


@routes.get('/', response_model=List[RouteOut],
            description="Все маршруты с постраничной навигацией **без информации** о входящих в них точках")
async def get_routes(page_size: int = 20, page_num: int = 0):
    return await db_manager.get_all_routes(page_size, page_num)


@routes.get('/full', response_model=List[RouteOut],
            description="Все маршруты с постраничной навигацией. **Включает информацию и о точках в каждом маршруте**")
async def get_routes_full(page_size: int = 20, page_num: int = 0):
    result = await db_manager.get_all_routes(page_size, page_num)

    r = []
    for row in result:
        r.append(RouteOut(**row))
        r[len(r)-1].points = await db_manager.get_points_for_route(row.id)

    return r


@routes.get('/{id}/', response_model=RouteOut, description="Получить подробную информацию о маршруте")
async def get_route(id: int):
    route = await db_manager.get_route(id)
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")

    # Преобразуем результат в уже нужную нам модель
    r = RouteOut(**route)

    # И заполним данные по точкам маршрута
    # r.points = [
    #    {"id": 1, "ord": 10, "name": "Точка 1", "latitude": 34.12, "longitude": 45.56},
    #    {"id": 2, "ord": 20, "name": "Точка 2", "latitude": 74.12, "longitude": 65.56}
    # ]
    r.points = await db_manager.get_points_for_route(id)

    return r
