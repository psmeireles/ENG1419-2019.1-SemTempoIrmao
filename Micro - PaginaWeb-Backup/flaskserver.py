from flask import Flask, render_template
from flask_socketio import SocketIO,emit


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route("/")
def hello():
    return render_template("teste.html")

@socketio.on('json')
def handle_json(json):
    print('received json: ' + str(json))
    emit('teste',"chegou")

@socketio.on('leitura')
def handle_json(json):
    emit("leitura","para porra")


if __name__ == '__main__':
    socketio.run(app)


