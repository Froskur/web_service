from app.model.route_model import PointNew
from typing import List
import random


async def get_optimal_track_for_route(points: List[PointNew]):
    # @Todo В моей логике сервиса расчет идёт тут, так как всё разделено и MVC у меня нет, и функции простые.

    random.shuffle(points)
    return points
