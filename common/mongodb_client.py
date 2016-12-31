from pymongo import MongoClient

MONGO_DB_HOST = 'localhost'
MONGO_DB_PORT = '27017'
DB_NAME = 'test'
USER_NAME = "tester"
PWD = "099484"


client = MongoClient('%s:%s' % (MONGO_DB_HOST, MONGO_DB_PORT))
mongodb = client[DB_NAME]

def getDB(db= DB_NAME):
    mongodb.authenticate(name=USER_NAME, password=PWD)
    return mongodb
