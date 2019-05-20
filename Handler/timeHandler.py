from Data import time


class TimeHandler:

    def __init__(self):
        self.model = None

    def parse(self, data):
        hour = data['hour']
        minutes = data['minutes']

        self.model = time.Time(hour, minutes)

        return self.model
