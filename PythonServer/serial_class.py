#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import serial
import time

class serial_client:

    def __init__(self):
        self.DEVICE = '/dev/cu.usbmodem143101'
        self.TIME_OUT = 1
        self.BAUD = 9600
        self.TIMEOUT= 1
        self.PARITY='N'
        self.STOPBITS= 1
        self.BYTESIZE= 8

    def connect(self):
        try:
            self.client = serial.Serial(self.DEVICE, baudrate=self.BAUD,
                                        bytesize=self.BYTESIZE, parity=self.PARITY,
                                        stopbits=self.STOPBITS, timeout=self.TIME_OUT) # Setando timeout 1s para a conexao
            #print "The port %s is available" % self.client

        except serial.serialutil.SerialException:
            print("The port is at use")
            self.client.close()
            self.client.open()

    def disconnect(self):
        self.client.close()

    def read(self):
        reply = self.client.readline()
        if not reply:
            return None
        else:
            reply = reply.decode("utf-8", errors='ignore').strip()
            print(reply)
        self.client.flushOutput()
        self.client.flushInput()
        return str(reply)

    def write(self, message):
        try:
            if self.client.in_waiting == 0:
                for i in message:
                    self.client.write(i.encode())
                    time.sleep(0.01)
            #self.client.write(message.encode())
        except serial.error as e:
            print(e)