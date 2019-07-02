#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import time
import threading
import serial
from socket_client_class import *
from serial_client_class import *






def write_to_arduino(serial_port):
    try:
        serial_port = serial.Serial(DEVICE,baudrate=BAUD, timeout=TIME_OUT) # Setando timeout 1s para a conexao
        print "The port %s is available" %serial_port

    except serial.serialutil.SerialException:
        print "The port is at use"
        serial_port.close()
        serial_port.open()

	time.sleep(1)
	message = "aaaaaaa\n"
    serial_port.write(message.encode("utf-8"))
	serial_port.close()

def start_game():
    socket = socket_client()
    socket.connect()
    serial = serial_client()
    serial.connect()


def main ():

    Python_To_Arduino_Thread = threading.Thread(target=write_to_arduino, args=(serial_port,))

    Python_To_Arduino_Thread.start()

main()