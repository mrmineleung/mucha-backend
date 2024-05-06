import datetime
from typing import List

from model.base import Base
from model.song import Song


class Playlist(Base):
    name: str | None = None
    description: str | None = None
    owner: str | None = None
    is_public: bool = False
    items: List[Song] = []

    class Settings:
        name = "playlists"
        # use_cache = True
        # cache_expiration_time = datetime.timedelta(seconds=10)
        # cache_capacity = 20
