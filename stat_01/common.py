"""The common module contains common functions and classes used by the other modules.
"""

def hello_world():
    """Prints "Hello World!" to the console.
    """
    print("Hello World!")


def add_marker(self, latitude, longitude, popup=None):
        marker = {
            'location': (latitude, longitude),
            'popup': popup
        }
        self.markers.append(marker)
        self.add_layer(marker)



import ipyleaflet

class Map(ipyleaflet.Map):

    def __init__(self, center=[20,0], zoom=2, **kwargs):
        super().__init__(center=center, zoom=zoom, **kwargs) 
        self.add_control(ipyleaflet.LayersControl())


