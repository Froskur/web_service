from typing import List
from fastapi import APIRouter, HTTPException
from app.db import db_manager

reports = APIRouter()


@reports.get('/summary', description="Сводная информация о пользователях и их маршрутах")
async def report_summary():
    r = {}

    # Немного PHP-ный стиль, но было лениво делать модель и в мелочах так удобно )
    for one in await db_manager.get_reports_summary():
        if not(one.author_id in r):
            r[one.author_id] = {
                "user_id": one.author_id,
                "name": one.user_name,
                "last_login": one.last_login,
                "route": []
            }

        # И теперь добавляем маршрут
        r[one.author_id]["route"].append({
            "id": one.id,
            "title": one.name,
            "short_num": one.short_num,
            "points_count":one.points_count,
            "created_at": one.created_at,
            "updated_at": one.updated_at
        })

    return [x for x in r.values()]
