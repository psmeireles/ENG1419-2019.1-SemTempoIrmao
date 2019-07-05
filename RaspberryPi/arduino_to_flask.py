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
endereco_end = endereco_base + "/gameOver"
endereco_hit = endereco_base + "/hit"
endereco_periodic_challenge_completed = endereco_base + "/correctPeriodicChallenge"
endereco_fix_challenge_completed = endereco_base + "/correctFixedChallenge"
endereco_new_fix_challenge = endereco_base + "/newFixedChallenge"
endereco_new_periodic_challenge = endereco_base + "/newPeriodicChallenge"


#CONSTANTES
CHALLENGES_MODES = ['countdown', 'wires', 'distance', 'light', 'genius']
FIX_MODES = ['wires', 'genius']
PERIODIC_MODES = ['countdown', 'distance', 'light']
WIRES_OPTIONS = ['1', '2', '3']
WIRES_ORDER = []
GENIUS_OPTIONS = ['1', '2', '3']
GENIUS_ORDER = []
DELTA_T = 600
GOAL = 5
COMPLETED_CHALLENGES = 0

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
    response = post(endereco_end, json={"win": CHALLENGES_COMPLETED == GOAL})
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
                challenge = generate_challenges(random.choice(FIX_MODES))
                challengeName = challenge.split(' ')[0]
                dados = {"minutes": DELTA_T/60, "seconds": DELTA_T%60, "challenge": challengeName, "params": [str(int(x)) for x in challenge.split(' ')[1:]]}
                response = post(endereco_start, json=dados)
                finish = Timer(TIMESUP, finish_game, args=[SERIAL_PORT, GAME_STARTED],)
                finish.start()
                SERIAL_PORT.write(challenge)

            elif(action == "hit"):
                if(HEARTS == 1 ):
                    HEARTS = (HEARTS - 1)
                    print("Perdeu o Jogo - TOTAL: " + str(HEARTS))
                    GAME_STARTED = False
                    reply_to_arduino = "end"
                    print(reply_to_arduino)
                    response = post(endereco_end, json={"win": False})
                    SERIAL_PORT.write(reply_to_arduino)

                else:
                    HEARTS = (HEARTS - 1)
                    print("Perdeu Vida - TOTAL: " + str(HEARTS))
                    dados = {"HEARTS": str(HEARTS)}
                    response = get(endereco_hit)

            elif(action == "finished"):
                print("Completou Desafio!" + challenge_completed + "\n")

                # Sending completed challenge to site
                dados = {"challenge": challenge_completed, "correct": True}
                address = endereco_fix_challenge_completed if challenge_completed in FIX_MODES else endereco_periodic_challenge_completed
                response = post(address, json=dados)

                # Generating new challenge
                mode = FIX_MODES if challenge_completed in FIX_MODES else PERIODIC_MODES
                if mode == FIX_MODES:
                    CHALLENGES_COMPLETED = CHALLENGES_COMPLETED + 1
                    if  CHALLENGES_COMPLETED == GOAL:
                        GAME_STARTED = False
                        response = post(endereco_end, json={"win": True})
                        SERIAL_PORT.write("end")
                        SERIAL_PORT.disconnect
                        continue
                    
                reply_to_arduino = generate_challenges(random.choice(mode))
                print(reply_to_arduino)

                # Sending new challenge to site
                address = endereco_new_fix_challenge if challenge_completed in FIX_MODES else endereco_new_periodic_challenge
                dados = {"challenge": challenge_completed, "params": [str(int(x)) for x in reply_to_arduino.split(' ')[1:]]}
                response = post(address, json=dados)

                SERIAL_PORT.write(reply_to_arduino)

            elif(action == "lost"): # Only periodic challenges send lost
                print("Nao Completou Desafio!")
                if(HEARTS == 1 ):
                    HEARTS = (HEARTS - 1)
                    print("Perdeu o Jogo - TOTAL: " + str(HEARTS))
                    GAME_STARTED = False
                    reply_to_arduino = "end"
                    print(reply_to_arduino)
                    response = post(endereco_end, json={"win": False})
                    SERIAL_PORT.write(reply_to_arduino)

                else:
                    HEARTS = (HEARTS - 1)
                    print("Perdeu Vida - TOTAL: " + str(HEARTS))
                    dados = {"HEARTS": str(HEARTS)}
                    response = get(endereco_hit)
                    dados = {"challenge": challenge_completed, "correct": False}
                    response = post(endereco_periodic_challenge_completed, json=dados)
                    reply_to_arduino = generate_challenges(random.choice(PERIODIC_MODES))
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