
class Time:

    def __init__(self, hour, minutes):
        self.hour = hour
        self.minutes = minutes

    def get_hour(self):
        return self.hour

    def get_minutes(self):
        return self.minutes

    def __str__(self):
        str_data = 'Time: ' + str(self.get_hour()) + ':' + str(self.get_minutes())
        return str_data
