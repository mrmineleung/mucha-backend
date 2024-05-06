import datetime

from model.base import Base


class Song(Base):
    album_image: str | None = None
    song_title: str | None = None
    song_artists: str | None = None
    album_name: str | None = None
    youtube_video_id: str | None = None
    youtube_video_title: str | None = None
    youtube_video_author: str | None = None
    song_id: str | None = None

    class Settings:
        name = "songs"
        use_cache = True
        cache_expiration_time = datetime.timedelta(seconds=3600)
        cache_capacity = 20
