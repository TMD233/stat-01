"""Main module."""
from ipyleaflet import Map, TileLayer, LayersControl, GeoJSON, ImageOverlay, basemaps, WidgetControl
from ipywidgets import Dropdown, Button, VBox
import requests
import json
from io import BytesIO
from zipfile import ZipFile
import geopandas as gpd
import rasterio

class CustomMap(Map):
    """
    This class inherits from ipyleaflet.Map to add enhanced functionality, including interactive basemap selection.
    """
    def __init__(self, center=(20, 0), zoom=2, **kwargs):
        super().__init__(center=center, zoom=zoom, **kwargs)
        self.add_control(LayersControl())
        self.initialize_ui()  

    def add_basemap(self, basemap_name):
        """
        Adds a predefined basemap to the map visualization based on the name provided.
        
        Args:
            basemap_name (str): Name of the basemap to add.
        """
        basemap_options = {
            'OpenStreetMap': basemaps.OpenStreetMap.Mapnik,
            'OpenTopoMap': basemaps.OpenTopoMap,
            'Esri World Imagery': basemaps.Esri.WorldImagery,
            'CartoDB Dark Matter': basemaps.CartoDB.DarkMatter
        }
        layer = TileLayer(url=basemap_options.get(basemap_name, basemaps.OpenStreetMap.Mapnik)['url'], name=basemap_name)
        self.clear_layers()
        self.add_layer(layer)

    def initialize_ui(self):
        """
        Initializes UI components for interactive basemap selection.
        """
        basemap_dropdown = Dropdown(
            options=[
                ('OpenStreetMap', 'OpenStreetMap'),
                ('OpenTopoMap', 'OpenTopoMap'),
                ('Esri World Imagery', 'Esri World Imagery'),
                ('CartoDB Dark Matter', 'CartoDB Dark Matter')
            ],
            value='OpenStreetMap',
            description='Basemaps:'
        )

        close_button = Button(description="Close Dropdown")

        dropdown_container = VBox([basemap_dropdown, close_button])

        def on_basemap_change(change):
            self.add_basemap(change['new'])

        basemap_dropdown.observe(on_basemap_change, names='value')

        def close_dropdown(b):
            dropdown_container.layout.display = 'none'

        close_button.on_click(close_dropdown)

        self.add_control(WidgetControl(widget=dropdown_container, position='topright'))

    def add_geojson(self, geojson_input):
        """
        Adds GeoJSON data to the map.
        
        Args:
            geojson_input (str | dict): URL, file path, or dictionary containing GeoJSON data.
        """
        if isinstance(geojson_input, str) and geojson_input.startswith('http'):
            response = requests.get(geojson_input)
            geojson_data = response.json()
        elif isinstance(geojson_input, str):
            with open(geojson_input) as f:
                geojson_data = json.load(f)
        elif isinstance(geojson_input, dict):
            geojson_data = geojson_input
        else:
            raise ValueError("Input must be a URL, file path, or dictionary.")
        geojson_layer = GeoJSON(data=geojson_data)
        self.add_layer(geojson_layer)

    def add_image(self, image_path, bounds):
        """
        Adds an image overlay to the map.
        
        Args:
            image_path (str): URL or local path to the image.
            bounds (tuple): Bounds of the image overlay as (lat_min, lon_min, lat_max, lon_max).
        """
        image_layer = ImageOverlay(url=image_path, bounds=bounds)
        self.add_layer(image_layer)



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