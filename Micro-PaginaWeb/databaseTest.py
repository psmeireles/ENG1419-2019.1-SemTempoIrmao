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
            "params": [2,3,1],
            "time_issued": {
                "minutes": 2,
                "seconds": 00
            },
            "completed": False
        },
        {
            "name": "genius",
            "params": [2,3,1],
            "time_issued": {
                "minutes": 2,
                "seconds": 00
            },
            "completed": True
        },
        {
            "name": "distance",
            "params": [10,30,10],
            "time_issued": {
                "minutes": 1,
                "seconds": 30
            },
            "completed": True
        },
        {
            "name": "light",
            "params": [10,30,10],
            "time_issued": {
                "minutes": 1,
                "seconds": 00
            },
            "completed": True
        },
        {
            "name": "countdown",
            "params": [10,20],
            "time_issued": {
                "minutes": 0,
                "seconds": 30
            },
            "completed": False
        }
    ],
    "finished": True 
    
}

#inserir
colecao.insert_one(data)

#apagar
#colecao.delete_many( { } )

