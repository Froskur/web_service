import os
import httpx

from typing import List
from fastapi import Depends, APIRouter, HTTPException
# from app.model.point_model import PointOut

URL_REPORTS = os.environ.get('REPORTS_SERVICE_HOST_URL') or 'http://localhost:8003/api/v1/reports/'
reports = APIRouter()


@reports.get('/summary', description="Сводная информация о пользователях и их маршрутах")
async def report_summary():
    # url = os.environ.get('POINTS_SERVICE_HOST_URL') or POINTS_SERVICE_HOST_URL
    r = httpx.get(f'{URL_REPORTS}summary')
    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=f"Error Reports-service: {r.json()}")

    return r.json()




