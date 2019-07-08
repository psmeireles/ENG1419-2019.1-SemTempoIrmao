# -*- coding: utf-8 -*-

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
            lastGame["finished"] = "Vitoria"
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
                    trueChallengeName = "Conexao de Fios"
                elif(challenge["name"] == "distance"):
                    trueChallengeName = "Manter distancia"
                elif(challenge["name"] == "genius"):
                    trueChallengeName = "Genius"
                elif(challenge["name"] == "light"):
                    trueChallengeName = "Alterar Luminosidade"
                elif(challenge["name"] == "countdown"):
                    trueChallengeName = "Apertar Botao"
                challengeNames = challengeNames + trueChallengeName+', '
            challengeNames=challengeNames[:-2]
            newGame["challenges"] = challengeNames
            challengeNames = ""
            if(result["finished"]):
                newGame["finished"] = "Vitoria"
            else:
                newGame["finished"] = "Derrota"
            games.append(newGame)
    return render_template("previousGames.html",games = games,lastGame = lastGame)

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

