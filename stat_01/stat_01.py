"""Main module."""

import ipyleaflet

class Map(ipyleaflet.Map):
    """
    This is map class that inherits from ipyleaflet. Map
    """
    def __init__(self, center=[20,0], zoom=2, **kwargs):
        """
        Args:
            center(list):Set the center of the map.
            zoom(int):Set zoom of the map.
        """
        super().__init__(center=center, zoom=zoom, **kwargs) 
        self.add_control(ipyleaflet.LayersControl())


"""
This function is use for finding dataset's mean.
"""
def calculate_mean(data):
    return sum(data) / len(data)
"""
This function is use for finding variance.
"""
def calculate_variance(data):
    mean = calculate_mean(data)
    variance = sum((x - mean) ** 2 for x in data) / len(data)
    return variance