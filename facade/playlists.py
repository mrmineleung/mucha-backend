import logging
from typing import List

from fastapi import HTTPException

from model.playlist import Playlist
from model.song import Song
from service import playlists as playlists_service

logger = logging.getLogger(__name__)


async def get_playlists(owner: str) -> List[Playlist]:
    return await playlists_service.get_playlist_by_owner(owner)


async def get_playlist_by_id(owner: str, playlist_id: str) -> dict | Playlist:
    playlist_data = await playlists_service.get_playlist_by_id(playlist_id)

    if not playlist_data:
        if playlist_data.owner != owner:
            raise HTTPException(status_code=400, detail="Not allow to access this resource")

    return playlist_data


async def get_public_playlist_by_id(playlist_id: str) -> dict | Playlist:
    playlist_data = await playlists_service.get_playlist_by_id(playlist_id)

    if playlist_data is not None:
        if playlist_data.is_public is not True:
            raise HTTPException(status_code=400, detail="Not allow to access this resource")

        return playlist_data
    else:
        raise HTTPException(status_code=400, detail="Playlist not found")


async def get_playlists_by_category(category: str) -> dict | List[Playlist]:
    if category == 'new-created':
        playlist = await playlists_service.get_new_public_playlist()
        if playlist is None:
            raise HTTPException(status_code=400, detail="Not found")
        return playlist
    elif category == 'new-updated':
        playlist = await playlists_service.get_latest_updated_public_playlist()
        if playlist is None:
            raise HTTPException(status_code=400, detail="Not found")
        return playlist
    elif category == 'melon' or category == 'billboard':
        playlist = await playlists_service.get_public_playlist_by_chart(category)
        if playlist is None:
            raise HTTPException(status_code=400, detail="Not found")
        return playlist
    else:
        raise HTTPException(status_code=400, detail="Not found")


async def create_playlist(owner: str, playlist: Playlist) -> dict | Playlist:
    existing_playlist = await playlists_service.get_playlist_by_owner(owner)

    logger.info(existing_playlist)

    if existing_playlist and existing_playlist['name'] == playlist['name']:
        raise HTTPException(status_code=400, detail="Duplicate playlist name")

    playlist_data = await playlists_service.create_playlist(owner, playlist)
    logger.info(existing_playlist)
    return playlist_data


async def save_to_playlist(owner: str, playlist_id: str, items: List[Song]) -> dict:
    existing_playlist: Playlist = await playlists_service.get_playlist_by_id(playlist_id)

    if existing_playlist:

        if existing_playlist.owner != owner:
            raise HTTPException(status_code=400, detail="Not allow to access this resource")

        playlist_items: List[Song] = existing_playlist.items
        new_items = playlist_items + [data for data in items if data not in playlist_items]
        existing_playlist.items = new_items
        await existing_playlist.save()
        return {"status": "success"}
    else:
        raise HTTPException(status_code=400, detail="Save to playlist failed")


async def delete_playlist(owner: str, playlist_id: str) -> dict:
    existing_playlist: Playlist = await playlists_service.get_playlist_by_id(playlist_id)

    if existing_playlist:

        if existing_playlist.owner != owner:
            raise HTTPException(status_code=400, detail="Not allow to access this resource")

        await existing_playlist.delete()
        return {"status": "success"}
    else:
        raise HTTPException(status_code=400, detail="Delete playlist failed")


async def delete_playlist_item(owner: str, playlist_id: str, song_id: str) -> dict:
    if song_id is None:
        raise HTTPException(status_code=400, detail="Missing song_id")

    existing_playlist: Playlist = await playlists_service.get_playlist_by_id(playlist_id)

    if existing_playlist:

        if existing_playlist.owner != owner:
            raise HTTPException(status_code=400, detail="Not allow to access this resource")

        playlist_items: List[Song] = existing_playlist.items
        new_items = list(filter(lambda x: x.song_id != song_id, playlist_items))

        if len(new_items) == len(playlist_items):
            raise HTTPException(status_code=400, detail="Playlist item not found")

        existing_playlist.items = new_items
        await existing_playlist.save()
        return {"status": "success"}
    else:
        raise HTTPException(status_code=400, detail="Delete playlist item failed")
