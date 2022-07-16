from typing import List
from fastapi import APIRouter, HTTPException
from app.model.point_model import PointOut, PointIn, PointUpdate
from app.db import db_manager

points = APIRouter()


@points.post('/', response_model=PointOut, status_code=201,
             description="Добавляет навигационную точку в базу. **Без проверок на существование**.")
async def create_point(m: PointIn):
    point_id = await db_manager.add_point(m)
    return db_manager.get_point(point_id)


# Можно было и объединить с обычным добавлением, но мне кажется это две разные задачи(потребности) и возможно какие-то
# проверки тут нужны будут ещё
@points.post('/batch', response_model=List[PointOut], status_code=201,
             description="Добавляет несколько точек базу. **Без проверок на существование**.")
async def create_point_batch(m_lst: List[PointIn]):

    # @Todo Тут можно ещё хотел сделать проверку чтобы возвращать точку, если она уже есть прямо с такими координатами
    r = []
    for m in m_lst:
        point_id = await db_manager.add_point(m)
        r.append(await db_manager.get_point(point_id))

    return r


@points.get('/', response_model=List[PointOut], description="Список всех навигационных точек с постраничной навигацией")
async def get_points(page_size: int = 50, page_num: int = 0):
    return await db_manager.get_all_points(page_size, page_num)


@points.get('/{id}/', response_model=PointOut)
async def get_point(id: int):
    point = await db_manager.get_point(id)
    if not point:
        raise HTTPException(status_code=404, detail="Point not found")
    return point


@points.put('/{id}/', response_model=PointOut)
async def update_point(id: int, m: PointUpdate):
    point = await db_manager.get_point(id)
    if not point:
        raise HTTPException(status_code=404, detail="Point not found")

    # Очистили передаваемы данные от значений с None, чтобы не обновлять их
    update_data = m.dict(exclude_unset=True)

    point_in_db = PointIn(**point)
    updated_point = point_in_db.copy(update=update_data)

    return await db_manager.update_point(id, updated_point)


@points.delete('/{id}/', response_model=None)
async def delete_point(id: int):
    point = await db_manager.get_point(id)
    if not point:
        raise HTTPException(status_code=404, detail="Point not found")

    # Todo: тут нужно ещё контроль на удаление точки которая в маршруте, BD не даст её удалить но не проверял с какой
    #       сообщением, чтобы это было красиво

    return await db_manager.delete_point(id)
