# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
# useful for handling different item types with a single interface

import json
import logging

from pymongo import MongoClient

import thumbnail_generator
from .youtube_api import search_data_from_youtube

logger = logging.getLogger(__name__)

class BillboardChartPipeline:
    def process_item(self, item, spider):
        return item


class JsonWriterPipeline(object):
    def process_item(self, item, spider):
        logger.debug(
            'JsonWriterPipeline : ' + json.dumps(dict(item), ensure_ascii=False))
        try:
            with open(spider.name + '.json', 'w') as fp:
                json.dump(dict(item), fp)
                return item
        except:
            return item


class SongMongoDBWriterPipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'music_charts')
        )

    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        for row in item['ranking']:
            song_title = row['song_title']
            song_artists = row['song_artists']
            album_image = row['album_image']

            song = self.db.songs.find_one({'song_title': song_title, 'song_artists': song_artists})

            youtube_video_id = ''
            youtube_video_title = ''
            youtube_video_author = ''
            new_song_id = ''

            if song is None:
                search_result = search_data_from_youtube(f'{song_title} {song_artists}')
                youtube_video_id = search_result['id']
                youtube_video_title = search_result['title']
                youtube_video_author = search_result['author']
                new_song = self.db.songs.insert_one(
                    {'song_title': song_title, 'song_artists': song_artists,
                     'album_image': album_image, 'youtube_video_id': youtube_video_id,
                     'youtube_video_title': youtube_video_title, 'youtube_video_author': youtube_video_author})
                new_song_id = str(new_song.inserted_id)

            if song is not None and song['youtube_video_id'] == '':
                search_result = search_data_from_youtube(f'{song_title} {song_artists}')
                youtube_video_id = search_result['id']
                youtube_video_title = search_result['title']
                youtube_video_author = search_result['author']
                self.db.songs.update_one(
                    {'song_title': song_title, 'song_artists': song_artists, 'album_image': album_image,
                     'youtube_video_id': ''},
                    {'$set': {'song_title': song_title, 'song_artists': song_artists, 'album_image': album_image,
                              'youtube_video_id': youtube_video_id,
                              'youtube_video_title': youtube_video_title,
                              'youtube_video_author': youtube_video_author}})

            if song is not None and 'youtube_video_id' in song and song['youtube_video_id'] != '':
                row['youtube_video_id'] = song['youtube_video_id']
                row['youtube_video_title'] = song['youtube_video_title']
                row['youtube_video_author'] = song['youtube_video_author']
            else:
                row['youtube_video_id'] = youtube_video_id
                row['youtube_video_title'] = youtube_video_title
                row['youtube_video_author'] = youtube_video_author

            if song is not None:
                row['song_id'] = str(song['_id'])
            else:
                row['song_id'] = new_song_id
        return item


class RankingMongoDBWriterPipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'music_charts')
        )

    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        ranking = self.db.rankings.find_one(
            {'chart': item['chart'], 'type': item['type'], 'date': item['date']})
        if ranking is None:
            self.db.rankings.insert_one(item)

        item.pop('_id', None)
        return item

class PlaylistMongoDBWriterPipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'music_charts')
        )

    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        playlist = self.db.playlists.find_one({'name': f"{item['chart']} {item['type']}"})
        playlist_id = ''

        if playlist is None:
            result = self.db.playlists.insert_one({'created_at': datetime.datetime.now(),
                                                   'updated_at': datetime.datetime.now(),
                                                   'name': f"{item['chart']} {item['type']}",
                                                   'owner': item['chart'],
                                                   'description': f"{item['date']}",
                                                   'is_public': True,
                                                   'items': item['ranking']})
            playlist_id = result.inserted_id
        else:
            self.db.playlists.update_one(
                {'name': f"{item['chart']} {item['type']}"},
                {'$set': {'updated_at': datetime.datetime.now(),
                          'description': f"{item['date']}",
                          'items': item['ranking'],
                          }})
            playlist_id = playlist['_id']

        image_list = list(map(lambda x: x['album_image'], item['ranking'][:6]))
        thumbnail_generator.combine_images(2, 0, image_list, playlist_id)
        item.pop('_id', None)
        return item
