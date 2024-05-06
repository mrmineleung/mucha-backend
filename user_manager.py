import logging
import ssl
from typing import Optional

from beanie import PydanticObjectId
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.authentication.strategy import AccessTokenDatabase, DatabaseStrategy
from fastapi_users.db import BeanieUserDatabase, ObjectIDIDMixin

import send_email
from config import settings
from db import User, get_user_db, AccessToken, get_access_token_db
from enumerations import EmailType
from facade import playlists as playlists_facade
from model.playlist import Playlist
from httpx_oauth.clients.google import GoogleOAuth2

logger = logging.getLogger(__name__)

SECRET = settings.SECRET_KEY

google_oauth_client = GoogleOAuth2(
    settings.GOOGLE_OAUTH_CLIENT_ID,
    settings.GOOGLE_OAUTH_CLIENT_SECRET,
)

class UserManager(ObjectIDIDMixin, BaseUserManager[User, PydanticObjectId]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    ssl._create_default_https_context = ssl._create_unverified_context

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        logger.info(f"User {user.id} has registered.")
        playlist = await playlists_facade.create_playlist(str(user.id), Playlist(name="Default"))
        logger.info(f"Created playlist id: {playlist.id}")

        if user.username is None and user.oauth_accounts is not None:
            user.username = user.email
            await user.save()

    async def on_after_forgot_password(
            self, user: User, token: str, request: Optional[Request] = None
    ):
        logger.debug(f"User {user.id} has forgot their password. Reset token: {token}")
        await send_email.send_email_async(EmailType.FORGOT_PASSWORD, "Reset your password", user.email,
                                          {"username": user.username, "base_url": settings.BASE_URL, "token": token})

    async def on_after_request_verify(
            self, user: User, token: str, request: Optional[Request] = None
    ):
        logger.debug(f"Verification requested for user {user.id}. Verification token: {token}")
        await send_email.send_email_async(EmailType.EMAIL_VERIFICATION, "Verify your account", user.email,
                                          {"username": user.username, "base_url": settings.BASE_URL, "token": token})


async def get_user_manager(user_db: BeanieUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


def get_database_strategy(
        access_token_db: AccessTokenDatabase[AccessToken] = Depends(get_access_token_db),
) -> DatabaseStrategy:
    return DatabaseStrategy(access_token_db, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

database_auth_backend = AuthenticationBackend(
    name="database",
    transport=bearer_transport,
    get_strategy=get_database_strategy,
)

fastapi_users = FastAPIUsers[User, PydanticObjectId](get_user_manager, [database_auth_backend])

current_active_user = fastapi_users.current_user(active=True)
