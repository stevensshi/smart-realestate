from pymongo import MongoClient

MONGO_DB_HOST = 'localhost'
MONGO_DB_PORT = '27017'
DB_NAME = 'smart_realestate_view'

client = MongoClient('%s:%s'% (MONGO_DB_HOST, MONGO_DB_PORT))

def getDB(db= DB_NAME):
    mongodb = client[db]
    return mongodb
