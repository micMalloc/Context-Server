import json
from json import JSONDecodeError
from selenium import webdriver
from Handler import dateHandler, destinationHandler, sourceHandler, timeHandler, weatherHandler
from selenium.webdriver.common.keys import Keys

class ContextHandler:
    def __init__(self, data):

        self.handler_list = {
            'date': dateHandler.DateHandler(),
            'time': timeHandler.TimeHandler(),
            'src': sourceHandler.SourceHandler(),
            'dest': destinationHandler.DestinationHandler(),
            'whtr': weatherHandler.WeatherHandler()
        }

        self.parsed_data = {}

        try:
            self.data = json.loads(data)
            self.context_list = self.data['context']

        except JSONDecodeError:
            return None

    def match_handler(self, key):
        return self.handler_list[key]

    def data_to_str(self):
        print('Context Data')

        for key, value in self.parsed_data.items():
                print(str(value))

    def parse(self):

        for key, value in self.context_list.items():
            handler = self.match_handler(key)
            self.parsed_data[key] = handler.parse(value)

        key = 'whtr'
        handler = self.match_handler(key)

        date = self.parsed_data['date']
        source = self.parsed_data['src']
        destination = self.parsed_data['dest']
        time = self.parsed_data['time']

        self.parsed_data[key] = handler.parse(date, time, source, destination)

        self.request_to_osrm(source, destination)
        print(self.data_to_str())

    def request_to_osrm(self, source, destination):

        print(source)
        path = "/Users/heesu.lee/Downloads/chromedriver-2"
        driver = webdriver.Chrome(path)
        driver.implicitly_wait(3)

        driver.get('http://map.project-osrm.org/')

        start = driver.find_element_by_xpath('//*[@id="map"]/div[2]/div[2]/div/div[1]/div[1]/input')
        start.send_keys(str(source.get_latitude()) + ',' + str(source.get_longitude()))
        start.send_keys(Keys.RETURN)
        end = driver.find_element_by_xpath('//*[@id="map"]/div[2]/div[2]/div/div[1]/div[2]/input')
        end.send_keys(str(destination.get_latitude()) + ',' + str(destination.get_longitude()))
        end.send_keys(Keys.RETURN)
#http://map.project-osrm.org/?z=12&center=37.435612%2C127.134132&loc=37.365779%2C127.107865&loc=37.448699%2C127.126725&hl=en&alt=0