import logging

from fastapi import HTTPException

from enumerations import Charts
from model.song import Song
from service import rankings as rankings_service

logger = logging.getLogger(__name__)

async def get_song(song_id: str) -> Song | None:
    return await Song.get(song_id)

async def get_ranking_history(song_id: str, chart_name: str, chart_type: str, records: int):
    song = await get_song(song_id)
    history_list = await rankings_service.get_ranking_history_by_song(chart_name, chart_type, song.song_title, song.song_artists, records)
    history_list.reverse()
    for history in history_list:
        rank = list(filter(lambda x: x.song_title == song.song_title and x.song_artists == song.song_artists, history.ranking))
        history.ranking = rank
    return history_list