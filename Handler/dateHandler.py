from Data import date


class DateHandler:

    def __init__(self):
        self.model = None

    def parse(self, data):
        year = data['year']
        month = data['month']
        day = data['day']

        self.model = date.Date(year, month, day)

        return self.model
