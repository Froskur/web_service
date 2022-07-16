import os
import httpx

POINT_SERVICE_HOST_URL = 'http://localhost:8001/api/v1/points/'


def points_add(points):
    url = os.environ.get('POINT_SERVICE_HOST_URL') or POINT_SERVICE_HOST_URL
    return httpx.post(f'{url}batch', json=points)


