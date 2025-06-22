from fastapi import APIRouter

index_controller_router = APIRouter()

@index_controller_router.get('', status_code=200)
async def get_charts():
    return {}
