from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pymongo import MongoClient

from config import settings


client = MongoClient(settings.MONGO_URI)

jobstores = {
    'default': MongoDBJobStore(client=client)
}

scheduler = AsyncIOScheduler(jobstores=jobstores)
