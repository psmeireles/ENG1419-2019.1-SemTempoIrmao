from gameController import GameController

class CountdownModule(Task):
    def __init__(self, isPeriodic, interval, duration, description):
        Task.__init__(self, isPeriodic, interval, duration, description)
        GameController.sendMessageToArduino("countdown " + str(interval))