#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import time
import threading
import serial

DEVICE='/dev/cu.usbmodem14201'
TIME_OUT=100000
BAUD=9600

#CONSTANTS
COUNTDOWN = time.time()
TIMESUP = COUNTDOWN+10

# Iniciando conexao serial
serial_port = serial.Serial(DEVICE,baudrate=BAUD, timeout=TIME_OUT) # Setando timeout 1s para a conexao

# Time entre a conexao serial e o tempo para escrever (enviar algo)
time.sleep(1.0) # Entre 1.5s a 2s


def read_from_arduino(serial_port):
    while ((TIMESUP) - time.time() > 0):
        try:
            serial_port = serial.Serial(DEVICE,baudrate=BAUD, timeout=TIME_OUT) # Setando timeout 1s para a conexao
            print "The port %s is available" %serial_port

        except serial.serialutil.SerialException:
            print "The port is at use"
            serial_port.close()
            serial_port.open()
        print(time.time())
    	time.sleep(1)
    	texto_recebido = serial_port.readline().decode().strip()
        print texto_recebido
        serial_port.close()
    print("Acabou o tempo!\n")

def write_to_arduino(serial_port):
    try:
        serial_port = serial.Serial(DEVICE,baudrate=BAUD, timeout=TIME_OUT) # Setando timeout 1s para a conexao
        print "The port %s is available" %serial_port

    except serial.serialutil.SerialException:
        print "The port is at use"
        serial_port.close()
        serial_port.open()

	time.sleep(1)
	message = "a\n"
	serial_port.write(message.encode("UTF-8"))
	serial_port.close()


#Arduino_To_Python_Thread = threading.Thread(target=read_from_arduino, args=(serial_port,))
#Arduino_To_Python_Thread.start()

#Python_To_Arduino_Thread = threading.Thread(target=write_to_arduino, args=(serial_port,))
#Python_To_Arduino_Thread.start()
