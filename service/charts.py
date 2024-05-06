import json
import logging
from json import JSONDecodeError

from enumerations import Charts
# from extensions import mongo

from model.ranking import Ranking

logger = logging.getLogger(__name__)


async def get_available_charts():
    return await Ranking.distinct('chart', {})
    # return mongo.db.rankings.distinct('chart', {})


async def get_available_chart_type(chart_name: str):
    return await Ranking.distinct('type', {"chart": chart_name})
    # return mongo.db.rankings.distinct('type', {"chart": chart_name})


async def get_chart(chart_name: Charts, chart_type: str):
    charts = {Charts.MELON: _get_melon_chart, Charts.BILLBOARD: _get_billboard_chart, Charts.BUGS: None, Charts.FLO: None, Charts.YOUTUBE: None,
              Charts.SPOTIFY: None}

    data = charts[chart_name](chart_type)
    return data


def _get_billboard_chart(chart_type: str):
    if chart_type is not None:
        try:
            with open(f'billboard_chart_{chart_type.lower()}.json', 'r') as json_file:
                data = json.load(json_file)
            return data
        except (JSONDecodeError, FileNotFoundError):
            logger.error('No related json file found')
            return None
    else:
        logger.error('Chart type not defined')
        return None


def _get_melon_chart(chart_type: str):
    if chart_type is not None:
        try:
            with open(f'melon_chart_{chart_type.lower()}.json', 'r') as json_file:
                data = json.load(json_file)
            return data
        except (JSONDecodeError, FileNotFoundError):
            logger.error('No related json file found')
            return None
    else:
        logger.error('Chart type not defined')
        return None


if __name__ == '__main__':
    print(get_chart(Charts.MELON, 'TOP100'))
