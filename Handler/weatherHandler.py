from Data import weather
from pyowm import OWM
import requests


class WeatherHandler:

    def __init__(self):
        self._API_KEY = '950858deadcf72d0c78ea3e2cbcad020'
        self._API_CALL = 'https://api.openweathermap.org/data/2.5/forecast?appid=' + self._API_KEY
        self.owm = OWM(self._API_KEY)
        self.model = None

    def get_target_name(self, latitude, longitude):
        obs = self.owm.weather_at_coords(latitude, longitude)
        target_name = obs.get_location().get_name()
        return target_name

    def get_target_forecast(self, target_name):
        message = self._API_CALL + '&q=' + target_name

        json_data = requests.get(message).json()
        return json_data

    def parse(self, date, time, source, destination):

        target_name = self.get_target_name(destination.get_latitude(), destination.get_longitude())
        json_data = self.get_target_forecast(target_name)

        # The current date we are iterating through
        target_date = date.date_to_str()
        target_time = time.get_hour()

        min_dif = 9999

        data = {}

        # Iterates through the array of dictionaries named list in json_data
        for item in json_data['list']:

            # Time of the weather data received, partitioned into 3 hour blocks
            time = item['dt_txt']

            # Split the time into date and hour [2018-04-15 06:00:00]
            next_date, hour = time.split(' ')

            if target_date != next_date:
                continue

            # Grabs the first 2 integers from our HH:MM:SS string to get the hours
            hour = int(hour[:2])

            dif = abs(target_time - hour)

            if dif < min_dif:
                min_dif = dif
                data['description'] = item['weather'][0]['description']
                data['temperature'] = item['main']['temp'] - 273.15

        self.model = weather.Weather(data['description'], data['temperature'])

        return self.model
