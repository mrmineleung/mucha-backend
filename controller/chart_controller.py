from fastapi import APIRouter
from fastapi_cache.decorator import cache

from enumerations import Charts
from facade import charts as charts_facade

chart_controller_router = APIRouter()


@chart_controller_router.get('', status_code=200)
@cache(expire=3600, namespace="charts")
async def get_charts():
    return await charts_facade.get_charts()


@chart_controller_router.get('/{chart_name}', status_code=200)
@cache(expire=3600, namespace="charts")
async def get_chart_type(chart_name: Charts):
    return await charts_facade.get_chart_type(chart_name)


@chart_controller_router.get('/{chart_name}/types/{chart_type}', status_code=200)
async def get_chart_data_by_type(chart_name: Charts, chart_type: str, sort: str | None = "asc",
                                 position_from: str | None = None, position_to: str | None = None):
    return await charts_facade.get_chart(chart_name, chart_type,
                                         {"sort": sort, "position_from": position_from, "position_to": position_to})
