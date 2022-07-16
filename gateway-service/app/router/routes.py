import os
import httpx
from datetime import datetime

from fastapi import Depends, APIRouter, HTTPException

from typing import List

from app.model.point_model import PointNew
from app.model.route_model import RouteIn, RouteOut, RouteUpdate
from app.model.user_model import User

from app.util import helper, auth

routes = APIRouter()
URL_ROUTE = os.environ.get('ROUTE_SERVICE_HOST_URL') or 'http://localhost:8002/api/v1/routes/'


@routes.get('/', response_model=List[RouteOut],
            description="Все маршруты с постраничной навигацией **без информации** о входящих в них точках")
async def get_routes(page_size: int = 20, page_num: int = 0):
    r = httpx.get(f'{URL_ROUTE}')
    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=f"Error Point-service: {r.json()}")

    return r.json()


@routes.get('/full', response_model=List[RouteOut],
            description="Все маршруты с постраничной навигацией. **Включает информацию и о точках в каждом маршруте**")
async def get_routes_full(page_size: int = 20, page_num: int = 0):
    r = httpx.get(f'{URL_ROUTE}full')
    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=f"Error Route-service: {r.json()}")

    return r.json()


@routes.get('/{id}/', response_model=RouteOut, description="Получить подробную информацию о маршруте")
async def get_route(id: int):
    r = httpx.get(f'{URL_ROUTE}{id}/')
    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=f"Error Route-service: {r.json()}")

    return r.json()


@routes.post('/optimal', response_model=List[PointNew],
             description="Считаем оптимальный маршрут для набора точек. Выдача будет содержать те же точки, но в другом порядке.")
async def optimal_route(p: List[PointNew]):
    r = httpx.post(f'{URL_ROUTE}optimal', json=[x.dict() for x in p])
    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=f"Error Route-service: {r.json()}")

    return r.json()


@routes.post('/', response_model=RouteOut, status_code=201, description="Создает новый маршрут с набором точек")
async def create_route(m: RouteIn, current_user: User = Depends(auth.get_current_active_user)):

    #raise HTTPException(status_code=406, detail=f"Error Route-service: {current_user}")

    # Что-то не увидел встроенного метода по переводу всей модели в диск
    model_dict = helper.model_full_convert_to_dict(m)
    model_dict['author_id'] = current_user.id

    r = httpx.post(f'{URL_ROUTE}', json=model_dict)
    if r.status_code != 201:
        raise HTTPException(status_code=r.status_code, detail=f"Error Route-service: {r.json()}")

    return r.json()







