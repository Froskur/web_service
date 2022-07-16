from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


# Модель для вставки, обязательны только координаты
class PointIn(BaseModel):
    name: Optional[str] = "New Point"
    latitude: float = Field(description="Широта в градусах", ge=-90.0, le=90.0)
    longitude: float = Field(description="Долгота в градусах", ge=-180.0, le=180.0)


# Модель для вывода, добавляем id и служебные поля
class PointOut(PointIn):
    id: int
    updated_at: datetime
    created_at: datetime


# Модель для обновления. Имя может быть опущено, updated_at меням дефолтно
class PointUpdate(PointIn):
    name: Optional[str]
    latitude: Optional[float] = Field(description="Широта в градусах", ge=-90.0, le=90.0)
    longitude: Optional[float] = Field(description="Долгота в градусах", ge=-180.0, le=180.0)


# Модель для добавления точки в маршрут
class PointNew(BaseModel):
    name: str = Field(description="Название точки, будет создана если её нет")
    latitude: float = Field(description="Широта в градусах", ge=-90.0, le=90.0)
    longitude: float = Field(description="Долгота в градусах", ge=-180.0, le=180.0)


# Модель для вывода точек в составе маршрута
class PointOutInRoute(BaseModel):
    id: int
    name: str
    ord: int = Field(description="Порядок следования точки в маршруте")
    latitude: float = Field(description="Широта в градусах", ge=-90.0, le=90.0)
    longitude: float = Field(description="Долгота в градусах", ge=-180.0, le=180.0)

