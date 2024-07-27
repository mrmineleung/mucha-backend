import datetime

from model.base import Base


class Thumbnail(Base):
    playlist_id: str | None = None
    image: str | None = None

    class Settings:
        name = "thumbnails"
        use_cache = True
        cache_expiration_time = datetime.timedelta(seconds=10)
        cache_capacity = 20
