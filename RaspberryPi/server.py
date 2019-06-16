from flask import Flask

app = Flask(__name__)

@app.route("/")
def start_game():
    return "Bem-vindo!"
    gc = gameController()
    gc.module1()
    gc.module2()
    gc.module3()

app.run(port=5000, debug=False)
