
from flask import Flask, render_template, request
from flask_socketio import SocketIO,emit
from pymongo import MongoClient,DESCENDING

app = Flask(__name__,static_url_path='/static')
socketio = SocketIO(app)
cliente = MongoClient("localhost", 27017)
banco = cliente["SemTempoIrmao"]
colecao = banco["Games"]

#Renderizacao de paginas 


@app.route("/")
def game():
    return render_template("jogo.html")

@app.route("/previousGames")
def history():
    #Pegando dados do ultimo jogo
    lastGame = {}
    challenges = []
    order = [["date", DESCENDING]]
    lastResult = colecao.find_one({},sort=order)
    if(lastResult != None):
        minutes = str(lastResult["time"]["minutes"]).zfill(2)
        seconds = str(lastResult["time"]["seconds"]).zfill(2)
        lastGame["time"] =  minutes + ':' + seconds
        lastGame["challenges"] = lastResult["challenges"]
        for challenge in lastGame["challenges"]:
            minutes = str(challenge["time_issued"]["minutes"]).zfill(2)
            seconds = str(challenge["time_issued"]["seconds"]).zfill(2)
            challenge["time_issued"] = minutes + ':' + seconds
        if(lastResult["finished"]):
            lastGame["finished"] = "Vitória"
        else:
            lastGame["finished"] = "Derrota"
    
    #Pegando dados de todos os jogos
    games = []
    challengeNames = ""
    results = list(colecao.find({},sort=order))
    if len(results) !=0:
        for result in results:
            newGame = {}
            minutes = str(result["time"]["minutes"]).zfill(2)
            seconds = str(result["time"]["seconds"]).zfill(2)
            newGame["time"] =  minutes + ':' + seconds
            for challenge in result["challenges"]:
                if(challenge["name"] == "wires"):
                    trueChallengeName = "Conexão de Fios"
                elif(challenge["name"] == "distance"):
                    trueChallengeName = "Manter distância"
                elif(challenge["name"] == "genius"):
                    trueChallengeName = "Genius"
                elif(challenge["name"] == "light"):
                    trueChallengeName = "Alterar Luminosidade"
                elif(challenge["name"] == "countdown"):
                    trueChallengeName = "Apertar Botão"
                challengeNames = challengeNames + trueChallengeName+','
            challengeNames=challengeNames[:-1]
            newGame["challenges"] = challengeNames
            challengeNames = ""
            if(result["finished"]):
                newGame["finished"] = "Vitória"
            else:
                newGame["finished"] = "Derrota"
            games.append(newGame)
    return render_template("previousGames.html",games = games,lastGame = lastGame)

#Evento de inicio do jogo:Responsável por comecar o timer da página e mostrar o primeiro desafio fixo
#Deve enviar: Nome do primeiro Desafio Fixo (string) + parametros
# @app.route("/start",  methods=['POST'])
# def startGame():
#     content = request.json
#     socketio.emit("start",content)
#     return "Game Started!"

# #Evento que adiciona um novo desafio Fixo
# #Deve enviar: Nome do Desafio Fixo a ser adicionado (string)
# @app.route('/newFixedChallenge', methods=['POST'])
# def newFixedChallenge():
#     content = request.json
#     socketio.emit("newFixedChallenge",content)
#     return "New Fixed Challenge!"

# #Evento que adiciona um novo desafio Periodico.
# #Deve enviar: Nome do Desafio Periodico a ser adicionado (string)
# @app.route('/newPeriodicChallenge' , methods=['POST'])
# def newPeriodicChallenge():
#     content = request.json
#     print(content)
#     socketio.emit("newPeriodicChallenge",content)
#     return "New Periodic Challenge!"




# #Evento que informa se o atual desafio Fixo foi cumprido ou nao.Pagina usa essa informaçao para decrementar
# #uma vida do player caso ele tenha errado.
# #Deve enviar: True se acertou e False se errou (bool)
# @app.route('/correctFixedChallenge', methods=['POST'])
# def correctFixedChallenge():
#     content = request.json
#     print(content)
#     socketio.emit("correctFixedChallenge", content)
#     return "Fixed Challenge Corrected"


# #Evento que informa que o player nao cumpriu um dos desafios periodicos.Pagina usa essa informaçao para decrementar uma vida do player.
# #Deve enviar: Numero do desafio que nao foi realizado (inteiro entre 0 e numDesafiosPeriodicos-1) 
# @app.route('/correctPeriodicChallenge', methods=['POST'])
# def correctPeriodicChallenge():
#     content = request.json
#     socketio.emit("correctPeriodicChallenge", content)
#     return "Periodic Challenge Corrected"



# #Evento que informa o fim do jogo. Ao receber esse evento, a pagina para o timer e exibe uma mensagem de vitoria/derrota
# #Deve enviar: True se venceu o jogo ou False se perdeu (bool)
# @app.route('/gameOver', methods=['POST'])
# def gameOver():
#     content = request.json
#     socketio.emit("gameOver",content)
#     return "Game Over"

@app.route('/<string:socketChannel>', methods=['POST'])
def gameOver(socketChannel):
    content = request.json
    socketio.emit(socketChannel,content)
    return socketChannel


@app.route('/hit')
def loseLife():
    socketio.emit("loseLife","")
    return "Lost Life"



if __name__ == '__main__':
    app.run(port=5000)

