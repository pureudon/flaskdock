import pymongo
import os

class Database(object):
    # URI = os.environ['DB_PORT_27017_TCP_ADDR']
    URI = "mongodb://db:27017"
    # URI = "mongodb://127.0.0.1:27017"
    # URI = "mongodb://localhost:27017"

    DATABASE = None

#    def __init__(self):
#        self.uri = ""
#        self.database = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['fullstack']

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        data = Database.DATABASE[collection].find_one(query)
        return data

    @staticmethod
    def update(collection, query, data):
        Database.DATABASE[collection].update(query, data, upsert=True)

    @staticmethod
    def remove(collection, query):
        Database.DATABASE[collection].remove(query)

