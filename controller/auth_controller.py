from fastapi import APIRouter

from config import settings
from model.user import UserRead, UserCreate
from user_manager import fastapi_users, database_auth_backend, google_oauth_client

auth_controller_router = APIRouter()

auth_controller_router.include_router(
    fastapi_users.get_auth_router(database_auth_backend, requires_verification=True),
)
auth_controller_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
)
auth_controller_router.include_router(
    fastapi_users.get_reset_password_router(),
)
auth_controller_router.include_router(
    fastapi_users.get_verify_router(UserRead),
)

auth_controller_router.include_router(
    fastapi_users.get_oauth_router(google_oauth_client, database_auth_backend, settings.SECRET_KEY,
                                   is_verified_by_default=True, redirect_url=settings.GOOGLE_OAUTH_REDIRECT_URL),
    prefix="/google",
    tags=["auth"],
)
