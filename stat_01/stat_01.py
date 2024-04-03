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
        if basemap == 'OpenStreetMap':
            folium.TileLayer('OpenStreetMap').add_to(self.map)
        elif basemap.startswith('http'):
            folium.TileLayer(basemap).add_to(self.map)
        else:
            print("Basemap not recognized. Using OpenStreetMap as default.")
            folium.TileLayer('OpenStreetMap').add_to(self.map)

    def show(self):
        return self.map
    def add_geojson(self, geojson_input):
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