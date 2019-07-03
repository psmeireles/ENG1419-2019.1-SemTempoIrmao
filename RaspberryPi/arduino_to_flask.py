import time
import random
from requests import *
from threading import Timer
from serial_class import *

random.seed(a=None)
endereco = "http://127.0.0.1"
port = "5000"
endereco_base = "http://127.0.0.1" + ":" + port

endereco_home = endereco_base + "/home"
endereco_start = endereco_base + "/start"
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
        return CHALLENGES_MODES[0] + " "  + "%02d" % seconds + " " + "%02d" % duration

    elif(challenge_instance == "wires"):

        for x in range(1,4):
            global WIRES_OPTIONS
            choice = random.choice(WIRES_OPTIONS)
            WIRES_OPTIONS.remove(choice)
            WIRES_ORDER.append(choice)
        WIRES_OPTIONS = ['1', '2', '3']
        duration = random.randint(20, 99)
        return CHALLENGES_MODES[1] + " " + WIRES_ORDER[0] + " " + WIRES_ORDER[1] + " " + WIRES_ORDER[2] + " " + "%02d" % duration

    elif (challenge_instance == "distance"):

        distance_max = random.randint(1, 50)
        distance_min = random.randint(1, distance_max)
        duration = random.randint(20, 99)
        return CHALLENGES_MODES[2] + " "  + "%02d" % distance_min + " " + "%02d" % distance_max + " " + "%02d" % duration

    elif (challenge_instance == "light"):

        light_max = random.randint(50,100)
        light_min = random.randint(0, light_max)
        duration = random.randint(5, 30)
        return CHALLENGES_MODES[3] + " "  + "%04d" % light_min + " " + "%04d" % light_max + " " + "%02d" % duration

    elif (challenge_instance == "genius"):

        while(len(GENIUS_ORDER) < 5):
            element = str(random.choice(GENIUS_OPTIONS))
            if(len(GENIUS_ORDER) == 0 ):
                GENIUS_ORDER.append(element)
            else:
                if(GENIUS_ORDER[-1] != element):
                    GENIUS_ORDER.append(element)
        light_interval = str(500)
        return CHALLENGES_MODES[4] + " "  + GENIUS_ORDER[0] + " " + GENIUS_ORDER[1] + " " + GENIUS_ORDER[2] + " " + GENIUS_ORDER[3] + " " + GENIUS_ORDER[4] + " " + light_interval 

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
            parts = reply.split(" ")

            if(len(parts) > 1):
                action = parts[0]
                challenge_completed = parts[1]

            else:
                action = reply

            if(action == "start"):
                GAME_STARTED = True
                COUNTDOWN = time.time()
                TIMESUP = (COUNTDOWN + DELTA_T)
                dados = {"minutes": DELTA_T/60, "seconds": DELTA_T%60, "challenge": "genius"}
                response = post(endereco_start, json=dados)
                finish = Timer(TIMESUP, finish_game, args=[SERIAL_PORT, GAME_STARTED],)
                finish.start()
                challenge = generate_challenges("wires")
                SERIAL_PORT.write(challenge)

            elif(action == "hit"):
                if(HEARTS == 0 ):
                    print("Perdeu o Jogo - TOTAL: " + str(HEARTS))
                    GAME_STARTED = False
                    reply_to_arduino = "end"
                    print(reply_to_arduino)
                    response = get(endereco_end)
                    SERIAL_PORT.write(reply_to_arduino)

                else:
                    HEARTS = (HEARTS - 1)
                    print("Perdeu Vida - TOTAL: " + str(HEARTS))
                    dados = {"HEARTS": str(HEARTS)}
                    response = post(endereco_base, dados)

            elif(action == "finished"):
                print("Completou Desafio!" + challenge_completed)
                reply_to_arduino = generate_challenges(random.choice(CHALLENGES_MODES))
                print(reply_to_arduino)
                dados = {"CHALLENGE_COMPLETED": str(challenge_completed)}
                response = post(endereco_challenge_completed, dados)
                SERIAL_PORT.write(reply_to_arduino)

            elif(action == "lost"):
                print("Nao Completou Desafio!")
                if(HEARTS == 0 ):
                    print("Perdeu o Jogo - TOTAL: " + str(HEARTS))
                    GAME_STARTED = False
                    reply_to_arduino = "end"
                    print(reply_to_arduino)
                    response = get(endereco_end)
                    SERIAL_PORT.write(reply_to_arduino)

                else:
                    HEARTS = (HEARTS - 1)
                    print("Perdeu Vida - TOTAL: " + str(HEARTS))
                    dados = {"HEARTS": str(HEARTS)}
                    response = post(endereco_base, dados)
                    reply_to_arduino = generate_challenges(random.choice(CHALLENGES_MODES))
                    print(reply_to_arduino)
                    SERIAL_PORT.write(reply_to_arduino)

            else:
                print("arduino: " + reply)
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