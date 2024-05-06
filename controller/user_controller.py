
from fastapi import APIRouter

from model.user import UserRead, UserUpdate
from user_manager import fastapi_users

user_controller_router = APIRouter()

user_controller_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    # prefix="/",
)
