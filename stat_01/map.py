import ipyleaflet
from ipyleaflet import basemaps

class CustomMap(Map):
    def __init__(self, center=(0, 0), zoom=10, **kwargs):
        super().__init__(center=center, zoom=zoom, **kwargs)

        self.markers = []

    def add_marker(self, latitude, longitude, popup=None):
        marker = {
            'location': (latitude, longitude),
            'popup': popup
        }
        self.markers.append(marker)
        self.add_layer(marker)

