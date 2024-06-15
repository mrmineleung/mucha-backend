from fastapi import APIRouter
from fastapi_cache.decorator import cache

from facade import songs as songs_facade

song_controller_router = APIRouter()


@song_controller_router.get('/{song_id}', status_code=200)
@cache(expire=3600, namespace="songs")
async def get_song(song_id: str):
    return await songs_facade.get_song(song_id)

@song_controller_router.get('/{song_id}/stats', status_code=200)
@cache(expire=1800, namespace="songs")
async def get_song_ranking_history(song_id: str, chart_name: str, chart_type: str, records: int = 30):
    return await songs_facade.get_ranking_history(song_id, chart_name, chart_type, records)


