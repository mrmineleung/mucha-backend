# from extensions import mongo
from model.ranking import Ranking


async def get_latest_ranking(chart_name: str, chart_type: str):
    return await Ranking.find_one({'chart': chart_name, 'type': chart_type}, sort=[('date', -1)])
    # return mongo.db.rankings.find_one({'chart': chart_name, 'type': chart_type}, sort=[('date', -1)])
