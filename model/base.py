from datetime import datetime
from beanie import Document, before_event, Insert, Replace, Update, SaveChanges


class Base(Document):
    created_at: datetime | None = datetime.now()
    updated_at: datetime | None = datetime.now()

    class Settings:
        is_root = False

    @before_event(Insert, Replace)
    def set_created_at(self):
        self.created_at = datetime.now()

    @before_event(Update, SaveChanges)
    def set_updated_at(self):
        self.updated_at = datetime.now()
