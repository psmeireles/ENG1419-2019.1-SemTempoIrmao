from pymongo import MongoClient, ASCENDING, DESCENDING

class database_client:

    def __init__(self):
        self.IP_HOST = "localhost"
        self.PORT = 27017
        self.DATABASE_NAME = "SemTempoIrmao"
        self.COLLECTION_NAME = "Games"
        self.CLIENT= None
        self.DATABASE = None
        self.COLLECTION= None

    def connect(self):
        self.CLIENT = MongoClient(self.IP_HOST, self.PORT)
        self.DATABASE = self.CLIENT[self.DATABASE_NAME]
        self.COLLECTION = self.DATABASE[self.COLLECTION_NAME]

    def send(self, data):
        self.COLLECTION.insert(data)
