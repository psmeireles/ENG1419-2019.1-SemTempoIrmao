import time
import threading
import random
from requests import get, post
from serial_client_class import *
import sys

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
        return "countdown " + "%.2f" % seconds + " " + "%.2f" % duration

    elif(challenge_instance == "wires"):

        for x in range(1,4):
            WIRES_ORDER.append(random.choice(WIRES_OPTIONS))
        duration = random.randint(20, 99)
        return "wires " + WIRES_ORDER[0] + " " + WIRES_ORDER[1] + " " + WIRES_ORDER[2] + " " + "%.2f" % duration

    elif (challenge_instance == "distance"):

        distance_max = random.randint(1, 50)
        distance_min = random.randint(1, distance_max)
        duration = random.randint(20, 99)
        return "distance " + str(distance_min) + " " + str(distance_max) + " " + "%.2f" % duration

    elif (challenge_instance == "light"):

        light_max = random.randint(1,1024)
        light_min = random.randint(0, light_max)
        duration = random.randint(20, 99)
        return "light " + str(light_min) + " " + str(light_max) + " " + "%.2f" % duration

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
        return "genius " + GENIUS_ORDER[0] + " " + GENIUS_ORDER[1] + " " + GENIUS_ORDER[2] + " " + GENIUS_ORDER[3] + " " + GENIUS_ORDER[4] + " " + light_interval + " " + "%.2f" % duration

    else:
        print("Modo de jogo nao encontrado!")


def read_from_arduino(serial_port):
    while (True):
        serial_port.connect()
        reply = serial_port.read()
        if reply is not None:
            reply.split(" ")
            action = reply[0]

            if(len(reply) > 1):
                challenge_completed = reply[1]

            if(action == "start"):
                COUNTDOWN = time.time()
                TIMESUP = "timer: " + str(COUNTDOWN + 10)
                serial_port.write(TIMESUP)

            elif(action == "hit"):
                print("Perdeu Vida!\n")

            elif(action == "finished"):
                print("Completou Desafio!" + challenge_completed + "\n")

        serial_port.disconnect

def start_game(serial_port):
    serial_port.connect()
    while (True):
        reply = serial_port.read()
        if(str(reply) == "start"):
            COUNTDOWN = time.time()
            TIMESUP = "timer: " + str(COUNTDOWN + 10)
            serial_port.write(TIMESUP)
            serial_port.disconnect()
            global GAME_STARTED
            GAME_STARTED = True
            return

def main():
    print(generate_challenges(random.choice(CHALLENGES_MODES)))
    serial_port = serial_client()

    listening_from_arduino = threading.Thread(target=read_from_arduino, args=(serial_port,))
    listening_from_arduino.start()

main()