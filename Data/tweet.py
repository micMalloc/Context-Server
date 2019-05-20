from Data import time


class Tweet:

    def __init__(self, hour, minutes, start, end):
        self.time = time.Time(hour, minutes)
        self.start = start
        self.end = end

    def get_section_name(self):
        return self.start, self.end

    def get_event_time(self):
        return self.time

    def __str__(self):
        return '[' + self.time.__str__() + '] ' + self.start + ' → ' + self.end
