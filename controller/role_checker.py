from user_manager import fastapi_users

from db import User
from typing import Annotated
from fastapi import Depends, HTTPException, status

current_active_verified_user = fastapi_users.current_user(active=True, verified=True)


class RoleChecker:
    def __init__(self, allowed_roles):
        self.allowed_roles = allowed_roles

    def __call__(self, user: Annotated[User, Depends(current_active_verified_user)]):
        if user.role in self.allowed_roles:
            return user
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You don't have enough permissions")
