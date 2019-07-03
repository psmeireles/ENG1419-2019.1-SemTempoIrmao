from flask import Flask, render_template
from flask_socketio import SocketIO,emit

app = Flask(__name__,static_url_path='/static')
socketio = SocketIO(app)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/jogo")
def hello():
    return render_template("pagina.html")


@app.route("/teste")
def fakeStart():
    socketio.emit("start","light")
    return "sextou"


#Evento de inicio do jogo:Responsável por comecar o timer da página e mostrar o primeiro desafio fixo
#Deve enviar: Nome do primeiro Desafio Fixo (string)
@socketio.on('start')
def startGame():
    emit("start","light")



#Evento que adiciona um novo desafio Fixo
#Deve enviar: Nome do Desafio Fixo a ser adicionado (string)
@socketio.on('newFixedChallenge')
def newFixedChallenge():
    emit("newFixedChallenge","distance")


#Evento que informa se o atual desafio Fixo foi cumprido ou nao.Pagina usa essa informaçao para decrementar
#uma vida do player caso ele tenha errado.
#Deve enviar: True se acertou e False se errou (bool)
@socketio.on('correctFixedChallenge')
def correctFixedChallenge():
    emit("correctFixedChallenge",True)

#Evento que adiciona um novo desafio Periodico.
#Deve enviar: Nome do Desafio Periodico a ser adicionado (string)
@socketio.on('newPeriodicChallenge')
def newPeriodicChallenge():
    emit("newPeriodicChallenge","light")

#Evento que informa que o player nao cumpriu um dos desafios periodicos.Pagina usa essa informaçao para decrementar uma vida do player.
#Deve enviar: Numero do desafio que nao foi realizado (inteiro entre 0 e numDesafiosPeriodicos-1) 
@socketio.on('correctPeriodicChallenge')
def correctPeriodicChallenge():
    emit("correctPeriodicChallenge","1 true")

@socketio.on('loseLife')
def loseLife():
    emit("loseLife","")

#Evento que informa o fim do jogo. Ao receber esse evento, a pagina para o timer e exibe uma mensagem de vitoria/derrota
#Deve enviar: True se venceu o jogo ou False se perdeu (bool)
@socketio.on('gameOver')
def gameOver():
    emit("gameOver",False)


if __name__ == '__main__':
    app.run(port=5000,debug=True)
