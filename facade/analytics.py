import logging

from service import analytics as analytics_service

logger = logging.getLogger(__name__)


async def add_play_history(user_id: str, item_id: str, type: str) -> None:
    if user_id == "None":
        user_id = "guest"
    await analytics_service.save_play_history(user_id, item_id, type)
