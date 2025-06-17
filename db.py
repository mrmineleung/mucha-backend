from datetime import datetime
from typing import List

from beanie import init_beanie, Document
import motor.motor_asyncio
from fastapi_users_db_beanie import BeanieUserDatabase, BeanieBaseUser, BaseOAuthAccount
from fastapi_users_db_beanie.access_token import BeanieAccessTokenDatabase, BeanieBaseAccessToken
from pydantic import Field

from config import settings
from model.play_history import PlayHistory
from model.playlist import Playlist
from model.ranking import Ranking
from model.song import Song
from model.thumbnail import Thumbnail


async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(
        settings.MONGO_URI
        , tls=True, tlsAllowInvalidCertificates=True
    )

    document_models = [User, AccessToken, Ranking, Song, Playlist, PlayHistory, Thumbnail]

    await init_beanie(database=client.music_charts, document_models=document_models, allow_index_dropping=True)


class OAuthAccount(BaseOAuthAccount):
    pass


class User(BeanieBaseUser, Document):
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    role: str | None = 'user'
    username: str | None = None
    oauth_accounts: List[OAuthAccount] = Field(default_factory=list)
    # pass


class AccessToken(BeanieBaseAccessToken, Document):
    pass


async def get_user_db():
    yield BeanieUserDatabase(User, OAuthAccount)


async def get_access_token_db():
    yield BeanieAccessTokenDatabase(AccessToken)
