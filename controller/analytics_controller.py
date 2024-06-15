import os
from typing import Annotated

from fastapi import Depends, APIRouter

from controller.role_checker import RoleChecker
from db import User
from facade import analytics as analytics_facade

analytics_controller_router = APIRouter()


@analytics_controller_router.put('/play_history/{history_type}/{item_id}', status_code=200)
async def add_play_history(
        user: Annotated[User, Depends(RoleChecker(allowed_roles=["guest", "user", "admin"]))],
        item_id: str,
        history_type: str = "song" or "playlist", ):
    return await analytics_facade.add_play_history(str(user.id), item_id, history_type)
