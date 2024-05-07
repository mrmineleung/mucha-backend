import os
from typing import Annotated, List

from fastapi import HTTPException, Depends, APIRouter

from fastapi.responses import FileResponse
from fastapi_cache.decorator import cache

from controller.role_checker import RoleChecker
from db import User
from model.playlist import Playlist
from model.song import Song
from facade import playlists as playlists_facade

playlist_controller_router = APIRouter()


@playlist_controller_router.get('/', status_code=200)
async def get_playlists(user: Annotated[User, Depends(RoleChecker(allowed_roles=["user", "admin"]))]):
    result = await playlists_facade.get_playlists(str(user.id))
    result = [playlist.model_dump(include={'id', 'name', 'is_public', 'created_at', 'updated_at', 'items'}) for playlist
              in result]
    return result


@playlist_controller_router.get('/{playlist_id}', status_code=200)
async def get_playlist(user: Annotated[User, Depends(RoleChecker(allowed_roles=["user", "admin"]))], playlist_id: str):
    result = await playlists_facade.get_playlist_by_id(str(user.id), playlist_id)
    result = result.model_dump(include={'id', 'name', 'is_public', 'items'})
    return result


@playlist_controller_router.put('/{playlist_id}', status_code=200)
async def add_to_playlist(user: Annotated[User, Depends(RoleChecker(allowed_roles=["user", "admin"]))],
                          playlist_id: str,
                          items: List[Song]):
    return await playlists_facade.save_to_playlist(str(user.id), playlist_id, items)


@playlist_controller_router.delete('/{playlist_id}', status_code=200)
async def delete_playlist(user: Annotated[User, Depends(RoleChecker(allowed_roles=["user", "admin"]))],
                          playlist_id: str):
    return await playlists_facade.delete_playlist(str(user.id), playlist_id)


@playlist_controller_router.delete('/{playlist_id}/item/{song_id}', status_code=200)
async def delete_playlist_item(user: Annotated[User, Depends(RoleChecker(allowed_roles=["user", "admin"]))],
                               playlist_id: str,
                               song_id: str):
    return await playlists_facade.delete_playlist_item(str(user.id), playlist_id, song_id)


@playlist_controller_router.post('/', status_code=201)
async def create_playlists(user: Annotated[User, Depends(RoleChecker(allowed_roles=["user", "admin"]))],
                           playlist: Playlist):
    created_playlist = await playlists_facade.create_playlist(str(user.id), playlist)
    created_playlist = created_playlist.model_dump(exclude={'_id'})
    return created_playlist


@playlist_controller_router.get('/category/{category}', status_code=200)
@cache(expire=3600, namespace="playlists")
async def get_playlists(category: str):
    result = await playlists_facade.get_playlists_by_category(category)
    result = [playlist.model_dump(include={'id', 'name', 'description', 'is_public', 'created_at', 'updated_at'}) for
              playlist
              in result]
    return result


@playlist_controller_router.get('/public/{playlist_id}', status_code=200)
@cache(expire=1800, namespace="playlists")
async def get_public_playlist(playlist_id: str):
    result = await playlists_facade.get_public_playlist_by_id(playlist_id)
    result = result.model_dump(include={'id', 'name', 'description', 'is_public', 'updated_at', 'items'})
    return result


@playlist_controller_router.get('/thumbnail/{playlist_id}', status_code=200)
@cache(expire=3600, namespace="playlists")
async def get_playlist_thumbnail(playlist_id: str):
    result: Playlist = await playlists_facade.get_public_playlist_by_id(playlist_id)
    if result is not None and os.path.isfile(f"thumbnail/{playlist_id}.png"):
        return FileResponse(f"thumbnail/{playlist_id}.png", media_type="image/png")
    else:
        raise HTTPException(status_code=404, detail='Thumbnail not found')
