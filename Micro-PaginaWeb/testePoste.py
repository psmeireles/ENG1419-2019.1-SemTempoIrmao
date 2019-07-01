from requests import post,get

endereco = "http://127.0.0.1:5000/startGame"

dados ={"nome":"light","tempo":"50"}

resposta = post(endereco, json=dados)

#resposta = get(endereco)

print(resposta.text)
