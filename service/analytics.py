import logging

from model.play_history import PlayHistory

logger = logging.getLogger(__name__)


async def save_play_history(user_id: str, item_id: str, type: str):
    play_history = PlayHistory(user_id=user_id, item_id=item_id, type=type)
    return await play_history.save()
