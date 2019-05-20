from Data import location


class Source(location.Location):

    def __init__(self, source, latitude, longitude):
        self.name = source
        self.latitude = latitude
        self.longitude = longitude
