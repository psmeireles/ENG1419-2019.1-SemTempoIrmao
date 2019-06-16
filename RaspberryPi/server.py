from flask import Flask
app = Flask(__name__)

@app.route("/")
def start_game():
    return "Bem-vindo!"


app.run(port=5000, debug=False)
