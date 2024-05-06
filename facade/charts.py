import logging

from fastapi import HTTPException

from enumerations import Charts
from service import charts as charts_service

logger = logging.getLogger(__name__)


async def get_chart(chart_name: Charts, chart_type: str, args: dict) -> dict:
    chart_data = await charts_service.get_chart(chart_name, chart_type)

    if chart_data is None:
        raise HTTPException(status_code=404, detail="Chart not found")

    logger.debug(f'Chart data: {chart_data}')

    sorting = args.get('sort', 'asc')

    if args.get('position_from') is not None and args.get('position_to') is not None:
        position_from = int(args['position_from'])
        position_to = int(args['position_to'])

        if position_to - position_from > 0:
            chart_data['ranking'] = chart_data['ranking'][position_from - 1:position_to:]

    if sorting != 'asc':
        chart_data.get('ranking', []).reverse()

    return chart_data


async def get_chart_type(chart_name: str) -> dict:
    chart_type = await charts_service.get_available_chart_type(chart_name)
    return {"chart": chart_name, "types": chart_type}


async def get_charts() -> dict:
    charts = await charts_service.get_available_charts()
    return {"charts": charts}
