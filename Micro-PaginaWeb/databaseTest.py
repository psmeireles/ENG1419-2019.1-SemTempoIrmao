from pymongo import MongoClient
from datetime import datetime, timedelta
cliente = MongoClient("localhost", 27017)
banco = cliente["SemTempoIrmao"]
colecao = banco["Games"]

#colecao.delete_many( { } )

data = {
    "date": datetime.now(),
    "time": {
        "minutes": 1,
        "seconds": 28
    },
    "challenges": [
        {
            "name": "wires",
            "params": ["2","3","1"],
            "time_issued": "20",
            "completed": False
        },
        {
            "name": "genius",
            "params": ["20","30","10"],
            "time_issued": "10",
            "completed": True
        },
        {
            "name": "distance",
            "params": ["20","40","10"],
            "time_issued": "25",
            "completed": True
        },
        {
            "name": "light",
            "params": ["20","30","10"],
            "time_issued": "80",
            "completed": True
        },
        {
            "name": "countdown",
            "params": ["20","30"],
            "time_issued": "20",
            "completed": False
        }
    ],
    "finished": True 
    
}

#inserir
colecao.insert_one(data)

#apagar
#colecao.delete_many( { } )