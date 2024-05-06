import datetime
from typing import List

from pydantic import BaseModel

from model.base import Base


class Rank(BaseModel):
    rank: str | None = None
    rank_changes_flow: str | None = None
    rank_changes_position: str | None = None
    album_image: str | None = None
    song_title: str | None = None
    song_artists: str | None = None
    album_name: str | None = None
    youtube_video_id: str | None = None
    youtube_video_title: str | None = None
    youtube_video_author: str | None = None


class Ranking(Base):
    chart: str | None = None
    type: str | None = None
    date: str | None = None
    ranking: List[Rank]

    class Settings:
        name = "rankings"
        use_cache = True
        cache_expiration_time = datetime.timedelta(seconds=3600)
        cache_capacity = 20
