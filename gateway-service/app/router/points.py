import os
import httpx

from typing import List
from fastapi import Depends, APIRouter, HTTPException
from app.model.point_model import PointOut


URL_POINTS = os.environ.get('POINTS_SERVICE_HOST_URL') or 'http://localhost:8001/api/v1/points/'
points = APIRouter()


@points.get('/', response_model=List[PointOut], description="Список всех навигационных точек с постраничной навигацией")
async def get_points(page_size: int = 50, page_num: int = 0):

    r = httpx.get(f'{URL_POINTS}')
    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=f"Error Point-service: {r.json()}")

    return r.json()



