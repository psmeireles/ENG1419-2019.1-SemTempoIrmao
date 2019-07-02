#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import serial

class serial_client:

    def __init__(self):
        self.DEVICE = '/dev/cu.usbmodem14101'
        self.TIME_OUT = 100000
        self.BAUD = 9600

    def connect(self):
        try:
            self.client = serial.Serial(self.DEVICE, baudrate=self.BAUD, timeout=self.TIME_OUT) # Setando timeout 1s para a conexao
            print "The port %s is available" % self.client

        except serial.serialutil.SerialException:
            print "The port is at use"
            self.client.close()
            self.client.open()

    def disconnect(self):
        self.client.close()

    def read(self):
        reply = self.client.readline()
        if not reply:
            return None
        else:
            reply = reply.decode().strip()
        return str(reply)

    def write(self, message):
        try:
            self.client.write(message.encode())
        except serial.error as e:
            print(e)