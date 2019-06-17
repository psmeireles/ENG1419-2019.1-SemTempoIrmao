from datetime import datetime, timedelta

# Task é uma interface para cada módulo
# Todo módulo vai herdar de task e implementar sua função que de fato executa o módulo


class Task:

    def __init__(self, isPeriodic, interval, duration, description):
        self.timeStarted = datetime.now()
        self.interval = interval
        self.duration = duration
        self.isPeriodic = isPeriodic
        self.isCompleted = False
        self.description = description