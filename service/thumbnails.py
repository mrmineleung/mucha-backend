import logging

from beanie.odm.operators.update.general import Set

from model.thumbnail import Thumbnail

logger = logging.getLogger(__name__)


async def get_thumbnail_by_playlist_id(playlist_id: str):
    return await Thumbnail.find_one(Thumbnail.playlist_id == playlist_id)


async def save_thumbnail(playlist_id: str, image: str):
    await Thumbnail.find_one(Thumbnail.playlist_id == playlist_id).upsert(
        Set({Thumbnail.image: image}),
        on_insert=Thumbnail(playlist_id=playlist_id, image=image)
    )
