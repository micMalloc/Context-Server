
class Weather:

    def __init__(self, description, temperature):
        self.description = description
        self.temperature = temperature

    def get_description(self):
        return self.description

    def get_temperature(self):
        return self.temperature

    def __str__(self):
        str_data = 'Weather: '
        str_data += self.get_description() + ' ' + str(self.get_temperature())
        return str_data
