import time
import threading
import random
from requests import get, post
from serial_client_class import *

endereco_base = "127.0.0.1"
endereco_home = endereco_base + "/home"
endereco_start = endereco_base + "/start"

#resposta = post(endereco_base, json=dados)


#CONSTANTES
CHALLENGES_MODES = ['countdown', 'wires', 'distance', 'light', 'genius']
WIRES_OPTIONS = ['1', '2', '3']
WIRES_ORDER = []
GENIUS_OPTIONS = ['1', '2', '3']
GENIUS_ORDER = []


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


def read_from_arduino(SERIAL_PORT , HEARTS):
    while (True):
        SERIAL_PORT.connect()
        reply = SERIAL_PORT.read()
        if reply is not None:

            if(len(reply.split(" ")) > 1):
                action = reply[0]
                challenge_completed = reply[1]

            else:
                action = reply

            if(action == "start"):
                COUNTDOWN = time.time()
                TIMESUP = "timer: " + str(COUNTDOWN + 10)
                SERIAL_PORT.write(TIMESUP)
                SERIAL_PORT.disconnect

            elif(action == "hit"):
                if(HEARTS == 0 ):
                    print("Perdeu o Jogo - TOTAL: " + str(HEARTS))
                else:
                    HEARTS = (HEARTS - 1)
                    print("Perdeu Vida - TOTAL: " + str(HEARTS))

            elif(action == "finished"):
                print("Completou Desafio!" + challenge_completed + "\n")

            elif(action == "lost"):
                print("Nao Completou Desafio!" + challenge_completed + "\n")
            SERIAL_PORT.disconnect

def main():
    HEARTS = 3
    print(generate_challenges(random.choice(CHALLENGES_MODES)))
    serial_port = serial_client()

    listening_from_arduino = threading.Thread(target=read_from_arduino, args=(serial_port, HEARTS))
    listening_from_arduino.start()

main()