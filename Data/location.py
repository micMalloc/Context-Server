
class Location:

    def __init__(self, name, latitude, longitude):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

    def get_location_name(self):
        return self.name

    def get_latitude(self):
        return self.latitude

    def get_longitude(self):
        return self.longitude

    def __str__(self):
        str_data = ''
        str_data += 'Location: ' + str(self.name) + ' '
        str_data += 'Latitude: ' + str(self.get_latitude()) + ' '
        str_data += 'Longitude: ' + str(self.get_longitude())
        return str_data
