from Data import location


class Destination(location.Location):

    def __init__(self, destination, latitude, longitude):
        self.name = destination
        self.latitude = latitude
        self.longitude = longitude

