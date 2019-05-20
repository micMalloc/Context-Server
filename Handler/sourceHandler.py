from Data import source


class SourceHandler:

    def __init__(self):
        self.model = None

    def parse(self, data):
        name = data['source']
        latitude = data['latitude']
        longitude = data['longitude']

        self.model = source.Source(name, latitude, longitude)

        return  self.model
