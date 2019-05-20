
class Date:

    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def get_year(self):
        return self.year

    def get_month(self):
        return self.month

    def get_day_of_month(self):
        return self.day

    def date_to_str(self):
        date = ''

        date += str(self.year)
        date += '-'
        if self.month < 10:
            date += '0'
        date += str(self.month)
        date += '-'
        if self.day < 10:
            date += '0'
        date += str(self.day)

        return date

    def __str__(self):
        str_data = 'Date:'
        str_data += self.date_to_str()
        return str_data
