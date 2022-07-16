from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from  app.model.point_model import PointNew, PointOutInRoute

# Модель для вставки, обязательны только координаты
class RouteIn(BaseModel):
    name: Optional[str] = Field(description="Название маршрута", default="New route")
    author_id: int = Field(description="ID пользователя, владельца маршрута")
    short_num: int = Field(description="Короткий номер (обозначение маршрута)")
    points: Optional[List[PointNew]] = Field(description="Список точек, входящих в маршрут. Порядок в которому идут точки, определяет порядок их следования в маршруте", default=None, min_items=2, max_items=10)


# Модель для вывода, добавляем id и служебные поля
class RouteOut(RouteIn):
    id: int
    points: Optional[List[PointOutInRoute]] = None
    updated_at: datetime
    created_at: datetime


# Модель для обновления. Имя может быть опущено, updated_at меням дефолтно
class RouteUpdate(RouteIn):
    name: Optional[str]
    short_num: Optional[int]



