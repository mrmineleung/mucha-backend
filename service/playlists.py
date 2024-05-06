import logging
from typing import List

from model.playlist import Playlist
from model.song import Song

logger = logging.getLogger(__name__)


async def get_playlist_by_owner(owner: str):
    return await Playlist.find(Playlist.owner == owner).to_list()


async def get_playlist_by_id(id: str):
    return await Playlist.get(id)


async def get_playlist_by_name(owner: str, playlist_name: str):
    return await Playlist.find(Playlist.owner == owner).find(Playlist.name == playlist_name).first_or_none()


async def create_playlist(owner: str, playlist: Playlist):
    playlist.owner = owner
    return await playlist.insert()


async def get_new_public_playlist():
    return await Playlist.find(Playlist.is_public == True).sort(-Playlist.created_at).limit(6).to_list()


async def get_latest_updated_public_playlist():
    return await Playlist.find(Playlist.is_public == True).sort(-Playlist.updated_at).limit(6).to_list()


async def get_public_playlist_by_chart(chart_name: str):
    return await Playlist.find(Playlist.is_public == True).find(
        {"owner": {'$regex': f'^{chart_name}$', "$options": 'i'}}).sort(
        -Playlist.created_at).limit(6).to_list()
