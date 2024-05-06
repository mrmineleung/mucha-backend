from beanie import Indexed, before_event, Insert, Replace, Update, SaveChanges
from datetime import datetime
from beanie import PydanticObjectId
from fastapi_users import schemas


class UserRead(schemas.BaseUser[PydanticObjectId]):
    role: str
    username: str | None = None


class UserCreate(schemas.BaseUserCreate):
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    role: str = 'user'
    username: Indexed(str, unique=True) | None = None

    @before_event(Insert, Replace)
    def set_created_at(self):
        self.created_at = datetime.now()

    @before_event(Update, SaveChanges)
    def set_updated_at(self):
        self.updated_at = datetime.now()


class UserUpdate(schemas.BaseUserUpdate):
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    username: Indexed(str, unique=True)

    @before_event(Insert, Replace)
    def set_created_at(self):
        self.created_at = datetime.now()

    @before_event(Update, SaveChanges)
    def set_updated_at(self):
        self.updated_at = datetime.now()
