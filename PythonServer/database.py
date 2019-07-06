from pymongo import MongoClient, ASCENDING, DESCENDING
IP_HOST = "192.168.215.164"
PORT = 27017
DATABASE_NAME = "ENG1419-G2"
COLLECTION_NAME = "SemTempoIrmao"

cliente = MongoClient(IP_HOST, PORT)
banco = cliente[DATABASE_NAME]
colecao = banco[COLLECTION_NAME]
