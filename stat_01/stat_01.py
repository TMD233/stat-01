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
    def add_basemap(self, basemap):
        """
        Adds a basemap to the map visualization.

        Parameters:
        - basemap (str): The name of the basemap to add. This can be a predefined name (e.g., 'OpenStreetMap') 
        or a URL to a custom TileLayer.

        Returns:
        None
        """
        if basemap == 'OpenStreetMap':
            folium.TileLayer('OpenStreetMap').add_to(self.map)
        elif basemap.startswith('http'):
            folium.TileLayer(basemap).add_to(self.map)
        else:
            print("Basemap not recognized. Using OpenStreetMap as default.")
            folium.TileLayer('OpenStreetMap').add_to(self.map)
            
    def show(self):
        """
        Renders and displays the current map with all added layers (basemaps, GeoJSON, shapefiles, etc.).

        Parameters:
        None

        Returns:
        A folium map object that can be displayed in Jupyter notebooks or saved as an HTML file.
        """
        return self.map
    def add_geojson(self, geojson_input):
        """
        Adds GeoJSON data to the map.

        Parameters:
        - geojson_input (str | dict): The GeoJSON data to add. Can be a file path, a URL to a GeoJSON file, 
        or a GeoJSON dictionary.

        Returns:
        None

        Exceptions:
        - ValueError: Raised if geojson_input is not a valid file path, URL, or dictionary.
        """
        if isinstance(geojson_input, str):
            if geojson_input.startswith('http'):
                # Handle URL
                response = requests.get(geojson_input)
                geojson_data = response.json()
            else:
                # Handle file path
                with open(geojson_input) as f:
                    geojson_data = f.read()
        elif isinstance(geojson_input, dict):
            geojson_data = geojson_input
        else:
            raise ValueError("Input must be a file path, URL, or dictionary.")
        
        folium.GeoJson(geojson_data).add_to(self.map)
    def add_shp(self, shp_path):
        """
        Adds shapefile data to the map.

        Parameters:
        - shp_path (str): The file path or URL to a zipped shapefile. If a URL is provided, 
        the method will attempt to download and extract the shapefile.

        Returns:
        None

        Exceptions:
        - ValueError: Might be implicitly raised by gpd.read_file or requests.get if the path or URL is invalid 
        (though not explicitly handled in the provided code).
        """
        if shp_path.startswith('http'):
            # Download the shapefile zip
            response = requests.get(shp_path)
            zip_file = ZipFile(BytesIO(response.content))
            shp_file = [name for name in zip_file.namelist() if name.endswith('.shp')][0]
            gdf = gpd.read_file(zip_file.open(shp_file))
        else:
            gdf = gpd.read_file(shp_path)
        
        folium.GeoJson(data=gdf["geometry"]).add_to(self.map)
    def add_vector(self, vector_data):
        """
        Adds vector data to the map. Can handle GeoPandas GeoDataFrames, GeoJSON files, or shapefiles.

        Parameters:
        - vector_data (gpd.GeoDataFrame | str): The vector data to add. Can be a GeoPandas GeoDataFrame, 
        a file path, or a URL to a GeoJSON or zipped shapefile.

        Returns:
        None

        Exceptions:
        - ValueError: Raised if vector_data is not a GeoDataFrame, file path, or URL, or if the file format is 
        not recognized.
        """
        if isinstance(vector_data, gpd.GeoDataFrame):
            folium.GeoJson(data=vector_data["geometry"]).add_to(self.map)
        elif isinstance(vector_data, str):
            if vector_data.endswith('.shp') or vector_data.startswith('http'):
                self.add_shp(vector_data)
            elif vector_data.endswith('.json') or vector_data.startswith('http'):
                self.add_geojson(vector_data)
            else:
                print("File format not recognized. Please provide a GeoDataFrame, GeoJSON, or Shapefile.")
        else:
            raise ValueError("Input must be a GeoDataFrame, file path, or URL.")
    def add_raster(self, cog_path, layer_name="COG Layer", colormap=None):
        """Add a Cloud Optimized GeoTIFF (COG) to the map.

        Args:
            cog_path (str): The path or URL to the COG file.
            layer_name (str): A name for the layer.
            colormap (str): Optional. A colormap name.
        """
        with rasterio.open(cog_path) as src:
            data = src.read(1) 
            bounds = [src.bounds.bottom, src.bounds.left, src.bounds.top, src.bounds.right]
            raster = RasterLayer(data=data, bounds=bounds, colormap=colormap)
            self.add_layer(raster)
    
    def add_image(self, image_path, bounds):
        """Add a static image or GIF to the map.

        Args:
            image_path (str): The path or URL to the image file.
            bounds (list): The geographical bounds [lat_min, lon_min, lat_max, lon_max] where the image should be placed.
        """
        image_overlay = ImageOverlay(url=image_path, bounds=bounds)
        self.add_layer(image_overlay)



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