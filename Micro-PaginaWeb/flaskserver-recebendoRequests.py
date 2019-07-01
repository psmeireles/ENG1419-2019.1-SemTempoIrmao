from flask import Flask, render_template,request
from flask_socketio import SocketIO,emit

app = Flask(__name__,static_url_path='/static')
socketio = SocketIO(app)

##Rotas para renderização de páginas
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/jogo")
def hello():
    return render_template("jogo.html")
    
########################

#Evento de inicio do jogo: Troca a página principal pela página do jogo
#Deve enviar: Nada
@app.route("/changePage")
def changePage():
    socketio.emit("changePage","")
    return "Changed Page!"

#Evento de inicio do jogo:Responsável por comecar o timer da página e mostrar o primeiro desafio fixo
#Deve enviar: Nome do primeiro Desafio Fixo (string) + parametros
@app.route("/startGame",  methods=['POST'])
def startGame():
    params = []
    content = request.json
    for key in content:
        params.append(content[key]);
    socketio.emit("start",params)
    return "Game Started!"

#Evento que adiciona um novo desafio Fixo
#Deve enviar: Nome do Desafio Fixo a ser adicionado e parametros(string)
@app.route("/newFixedChallenge",  methods=['POST'])
def newFixedChallenge():
    params = []
    content = request.json
    for key in content:
        params.append(content[key]);
    socketio.emit("start",params)
    return "Game Started!"



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
    app.run(port=5000)
