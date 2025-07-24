# from extensions import mongo
from model.ranking import Ranking, RankingHistoryView, RankingView


async def get_latest_ranking(chart_name: str, chart_type: str):
    return await Ranking.find_one({'chart': chart_name, 'type': chart_type}, sort=[('date', -1)], projection_model=RankingView)
    # return mongo.db.rankings.find_one({'chart': chart_name, 'type': chart_type}, sort=[('date', -1)])


async def get_ranking_by_date(chart_name: str, chart_type: str, date: str):
    return await Ranking.find_one({'chart': chart_name, 'type': chart_type, 'date': date})


async def get_ranking_by_days(chart_name: str, chart_type: str, days: int):
    return await Ranking.find({'chart': chart_name, 'type': chart_type}).limit(days).to_list()


async def get_ranking_history_by_song(chart_name: str, chart_type: str, song_title: str, song_artists: str,
                                      records: int):
    return await Ranking.find({
        'chart': chart_name,
        'type': chart_type,
        "ranking": {"$elemMatch": {"song_title": song_title, "song_artists": song_artists}}}).sort(
        -Ranking.date).project(RankingHistoryView).limit(records).to_list()
