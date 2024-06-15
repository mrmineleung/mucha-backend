import datetime
from model.base import Base


class PlayHistory(Base):
    user_id: str | None = None
    item_id: str | None = None
    type: str | None = None

    class Settings:
        name = "play_histories"
        use_cache = True
        cache_expiration_time = datetime.timedelta(seconds=3600)
        cache_capacity = 20
