from serial import Serial

class GameController:

    def __init__(self, lives, timeInSeconds):
        self.lives = lives
        self.time = timeInSeconds
        self.tasks = {}
        self.serial = Serial("/dev/serial0", baudrate=9600, timeout=0.01)
        self.modules = []

    @staticmethod
    def sendMessageToArduino(self, msg):
        self.serial.write(msg.encode("UTF-8"))

    def getMessageFromArduino(self):
        msg = self.serial.readline()
        if msg != "":
            msg = msg.decode().strip()
            print(msg)
            

    def initModule(self, module):
        module.init()
        self.modules.append(module)