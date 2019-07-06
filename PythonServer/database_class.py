from pymongo import MongoClient, ASCENDING, DESCENDING

class database_client:

    def __init__(self):
        self.IP_HOST = "192.168.215.164"
        self.PORT = 27017
        self.DATABASE_NAME = "ENG1419-G2"
        self.COLLECTION_NAME = "SemTempoIrmao"
        self.CLIENT= None
        self.DATABASE = None
        self.COLLECTION= None

    def connect(self):
        self.CLIENT = MongoClient(self.IP_HOST, self.PORT)
        self.DATABASE = self.CLIENT[self.DATABASE_NAME]
        self.COLLECTION = self.DATABASE[self.COLLECTION_NAME]

    def send(self, data):
        self.COLLECTION.insert(data)
