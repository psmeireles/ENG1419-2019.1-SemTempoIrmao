from database_class import *
db_client = database_client()
dados = {"date": "date", "time": {"minutes": 5, "seconds":10}, "challenges":[{"name": "teste","time_issued":,"params":,"completed":"true"}],"finished":"true"}
db_client.send(dados)
