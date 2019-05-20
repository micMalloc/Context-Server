from Data import destination


class DestinationHandler:

    def __init__(self):
        self.model = None

    def parse(self, data):
        name = data['destination']
        latitude = data['latitude']
        longitude = data['longitude']

        self.model = destination.Destination(name, latitude, longitude)

        return self.model
