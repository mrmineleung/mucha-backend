from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi_cache import FastAPICache

from controller.role_checker import RoleChecker
from db import User

admin_controller_router = APIRouter()


@admin_controller_router.delete('/cache', status_code=200)
async def clear_cache(_: Annotated[User, Depends(RoleChecker(allowed_roles=["admin"]))],
                      namespace: str | None = None, key: str | None = None):
    return await FastAPICache.clear(namespace=namespace, key=key)
