from flask import Flask
from modules.countdown import CountdownModule
from gameController import GameController

app = Flask(__name__)

@app.route("/")
def start_game():
    return "Bem-vindo!"
    gc = GameController(3, 180)
    
    gc.initModule(CountdownModule(True, 10, -1, "Countdown"))
    print(gc.modules)

app.run(port=5000, debug=False)

