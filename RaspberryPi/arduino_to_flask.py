import time
import random
from requests import *
from threading import Timer
from serial_class import *

endereco = "http://127.0.0.1"
port = "5000"
endereco_base = "http://127.0.0.1" + ":" + port

endereco_home = endereco_base + "/home"
endereco_start = endereco_base + "/startGame"
endereco_end = endereco_base + "/end"
endereco_challenge_completed = endereco_base + "/challenge_completed"


#CONSTANTES
CHALLENGES_MODES = ['countdown', 'wires', 'distance', 'light', 'genius']
WIRES_OPTIONS = ['1', '2', '3']
WIRES_ORDER = []
GENIUS_OPTIONS = ['1', '2', '3']
GENIUS_ORDER = []
DELTA_T = 600

def generate_challenges(challenge_instance):

    if(challenge_instance == "countdown"):

        duration = random.randint(15, 60) # dois digitos
        seconds = random.randint(5, duration)
        return CHALLENGES_MODES[0] + " "  + "%.2f" % seconds + " " + "%.2f" % duration

    elif(challenge_instance == "wires"):

        for x in range(1,4):
            WIRES_ORDER.append(random.choice(WIRES_OPTIONS))
        duration = random.randint(20, 99)
        return CHALLENGES_MODES[1] + " " + WIRES_ORDER[0] + " " + WIRES_ORDER[1] + " " + WIRES_ORDER[2] + " " + "%.2f" % duration

    elif (challenge_instance == "distance"):

        distance_max = random.randint(1, 50)
        distance_min = random.randint(1, distance_max)
        duration = random.randint(20, 99)
        return CHALLENGES_MODES[2] + " "  + str(distance_min) + " " + str(distance_max) + " " + "%.2f" % duration

    elif (challenge_instance == "light"):

        light_max = random.randint(1,1024)
        light_min = random.randint(0, light_max)
        duration = random.randint(20, 99)
        return CHALLENGES_MODES[3] + " "  + str(light_min) + " " + str(light_max) + " " + "%.2f" % duration

    elif (challenge_instance == "genius"):

        while(len(GENIUS_ORDER) < 5):
            element = str(random.choice(GENIUS_OPTIONS))
            if(len(GENIUS_ORDER) == 0 ):
                GENIUS_ORDER.append(element)
            else:
                if(GENIUS_ORDER[-1] != element):
                    GENIUS_ORDER.append(element)
        light_interval = str(500)
        duration = random.randint(5, 99)  # dois digitos
        return CHALLENGES_MODES[4] + " "  + GENIUS_ORDER[0] + " " + GENIUS_ORDER[1] + " " + GENIUS_ORDER[2] + " " + GENIUS_ORDER[3] + " " + GENIUS_ORDER[4] + " " + light_interval + " " + "%.2f" % duration

    else:
        print("Modo de jogo nao encontrado!")

def finish_game(SERIAL_PORT, GAME_STARTED):
    print("FINISH")
    GAME_STARTED = False
    SERIAL_PORT.connect()
    reply_to_arduino = "end"
    print(reply_to_arduino)
    SERIAL_PORT.write(reply_to_arduino)
    return


def read_from_arduino(SERIAL_PORT , GAME_STARTED, HEARTS):
    while (GAME_STARTED):
        SERIAL_PORT.connect()
        reply = SERIAL_PORT.read()
        if reply is not None:

            if(len(reply.split(" ")) > 1):
                action = reply[0]
                challenge_completed = reply[1]

            else:
                action = reply

            if(action == "start"):
                GAME_STARTED = True
                COUNTDOWN = time.time()
                TIMESUP = (COUNTDOWN + DELTA_T)
                dados = {"TIME": str(TIMESUP)}
                response = post(endereco_start, dados)
                print(response.txt)
                finish = Timer(TIMESUP, finish_game, args=[SERIAL_PORT, GAME_STARTED, ],)
                finish.start()
                SERIAL_PORT.disconnect

            elif(action == "hit"):
                if(HEARTS == 0 ):
                    print("Perdeu o Jogo - TOTAL: " + str(HEARTS))
                    GAME_STARTED = False
                    reply_to_arduino = "end"
                    print(reply_to_arduino)
                    response = get(endereco_end)
                    print(response.txt)
                    SERIAL_PORT.write(reply_to_arduino)

                else:
                    HEARTS = (HEARTS - 1)
                    print("Perdeu Vida - TOTAL: " + str(HEARTS))
                    dados = {"HEARTS": str(HEARTS)}
                    response = post(endereco_base, dados)
                    print(response.txt)

            elif(action == "finished"):
                print("Completou Desafio!" + challenge_completed)
                reply_to_arduino = generate_challenges(random.choice(CHALLENGES_MODES))
                print(reply_to_arduino)
                dados = {"CHALLENGE_COMPLETED": str(challenge_completed)}
                response = post(endereco_challenge_completed, dados)
                print(response.txt)
                SERIAL_PORT.write(reply_to_arduino)

            elif(action == "lost"):
                print("Nao Completou Desafio!")
                reply_to_arduino = generate_challenges(random.choice(CHALLENGES_MODES))
                print(reply_to_arduino)
                SERIAL_PORT.write(reply_to_arduino)
            SERIAL_PORT.disconnect


    finish.cancel()
    return False

def main():
    HEARTS = 3
    serial_port = serial_client()
    global GAME_STARTED
    GAME_STARTED = True
    return read_from_arduino(serial_port, GAME_STARTED, HEARTS)

main()