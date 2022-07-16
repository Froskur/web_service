import random
from app.model.point_model import PointIn
from app.db import db_manager
import asyncio
from app.db.db import metadata, database, engine

metadata.create_all(engine)


def generate_new_point(count: int = 5, predprecision: int = 8):
    min_latitude = -15
    max_latitude = 85
    min_longitude = -180
    max_longitude = 180

    for x in range(count):
        new_point = {
            'name': f'Точка {x+1}',
            'latitude': round(random.uniform(min_latitude, max_latitude), predprecision),
            'longitude': round(random.uniform(min_longitude, max_longitude), predprecision)
        }

        Point = PointIn(**new_point)
        # print(Point)

        # Снова хитрость для вызова асинхронной функции
        loop = asyncio.get_event_loop()
        loop.run_until_complete(db_manager.add_point(Point))



# Вызываем асинхронную функцию как синхронную, чтобы дождаться подключения
loop = asyncio.get_event_loop()
loop.run_until_complete(database.connect())

# Тут вызов генератора точек обычный
generate_new_point(10**6)
print("Ok!")
