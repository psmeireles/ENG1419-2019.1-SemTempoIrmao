from requests import post,get

endereco = "http://127.0.0.1:5000/gameOver"

endereco1 = "http://127.0.0.1:5000/start"

endereco3 = "http://127.0.0.1:5000/newFixedChallenge"

endereco4 = "http://127.0.0.1:5000/newPeriodicChallenge"

endereco5 = "http://127.0.0.1:5000/correctFixedChallenge"

endereco6 = "http://127.0.0.1:5000/correctPeriodicChallenge"

endereco7 = "http://127.0.0.1:5000/hit"

dados1 = {"minutes":2, "seconds": 0, "challenge": "wires","params":["1","2","3"]}

dados2 = {"win": True}

dados3 = {"challenge": "genius","params":["1","2","3"]}

dados4 = {"challenge": "light","params":["10","20","5"]}

dados5 = {"challenge": "wires","correct":True}

resposta = post(endereco5, json=dados5)



#resposta = get(endereco7)

print(resposta.text)
