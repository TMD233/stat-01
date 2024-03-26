
    def add_marker(self, latitude, longitude, popup=None):
        marker = {
            'location': (latitude, longitude),
            'popup': popup
        }
        self.markers.append(marker)
        self.add_layer(marker)