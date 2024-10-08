import os

import pandas as pd
import folium
from geopy.distance import geodesic

base_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
print(base_dir)
pollution_files = {
    'Belfast_Westlink': os.path.join(base_dir, 'csv', 'Belfast_Westlink_Pollution_Data.csv'),
    'Belfast_Stockmans_Lane': os.path.join(base_dir, 'csv', 'Belfast_Stockmans_Pollution_Data.csv'),
    'Belfast_Ormeau': os.path.join(base_dir, 'csv', 'Belfast_Ormeau_Pollution_Data.csv'),
    'Belfast_Newtownards': os.path.join(base_dir, 'csv', 'Belfast_Newtownards_Pollution_Data.csv'),
    'Belfast_Centre': os.path.join(base_dir, 'csv', 'Belfast_Centre_Pollution_Data.csv')
}


# Actual coordinates for the monitoring stations
monitoring_stations = {
    "Belfast Westlink": (54.591753, -5.949517),
    "Belfast Stockmans Lane": (54.572586, -5.974944),
    "Belfast Ormeau": (54.587516, -5.923780),
    "Belfast Newtownards": (54.596530, -5.901667),
    "Belfast Centre": (54.599650, -5.928833)
}

# Function to extract the key pollutants and calculate the average pollution for a zone
def calculate_average_pollution(file, pollutant_col_name):
    df = pd.read_csv(file)
    df = df[pd.to_numeric(df[pollutant_col_name], errors='coerce').notnull()]
    df[pollutant_col_name] = pd.to_numeric(df[pollutant_col_name])
    return df[pollutant_col_name].mean()

# Function to generate and save the map
def generate_pollution_tree_map():
    # Load the tree dataset
    tree_data = pd.read_csv(r'C:\Users\benmc\GitHub\hackathon\hackathon\csv\odTrees.csv', low_memory=False)

    # Define the grid cell size (approx. 1km in degrees)
    LAT_GRID_SIZE = 0.01  # Approx 1km in latitude
    LON_GRID_SIZE = 0.015  # Approx 1km in longitude

    # Create a map centered around the average latitude and longitude in the dataset
    belfast_map = folium.Map(location=[tree_data['LATITUDE'].mean(), tree_data['LONGITUDE'].mean()], zoom_start=12)

    # Function to calculate the grid cell for a given lat/lon
    def get_grid_cell(lat, lon, lat_grid_size, lon_grid_size):
        lat_cell = int(lat // lat_grid_size)
        lon_cell = int(lon // lon_grid_size)
        return lat_cell, lon_cell

    # Initialize a dictionary to count the trees in each grid cell
    grid_tree_counts = {}

    # Iterate through the dataset and count trees in each grid cell
    for _, row in tree_data.iterrows():
        lat, lon = row['LATITUDE'], row['LONGITUDE']
        cell = get_grid_cell(lat, lon, LAT_GRID_SIZE, LON_GRID_SIZE)

        if cell not in grid_tree_counts:
            grid_tree_counts[cell] = 0
        grid_tree_counts[cell] += 1

    # Create a function to check if a point is inside a circular zone (pollution radius)
    def is_in_pollution_zone(lat, lon, zone_center, zone_radius_km):
        distance = geodesic((lat, lon), zone_center).km
        return distance <= zone_radius_km

    # Adjust function to check if any corner of the grid cell is inside the pollution zone
    def is_cell_in_pollution_zone(lat_min, lat_max, lon_min, lon_max, zone_center, zone_radius_km):
        corners = [
            (lat_min, lon_min),
            (lat_min, lon_max),
            (lat_max, lon_min),
            (lat_max, lon_max)
        ]
        return any(is_in_pollution_zone(lat, lon, zone_center, zone_radius_km) for lat, lon in corners)

    # Function to determine cell color based on the number of trees
    def get_tree_color(tree_count, max_count):
        if tree_count == 0:
            return 'gray'  # Empty cells
        # Gradient from red to green based on tree density
        ratio = tree_count / max_count
        red = int(255 * (1 - ratio))
        green = int(255 * ratio)
        return f'#{red:02x}{green:02x}00'

    # Add the tree grid to the map, but exclude cells that overlap with pollution zones
    max_tree_count = max(grid_tree_counts.values())

    for (lat_cell, lon_cell), tree_count in grid_tree_counts.items():
        lat_min = lat_cell * LAT_GRID_SIZE
        lat_max = (lat_cell + 1) * LAT_GRID_SIZE
        lon_min = lon_cell * LON_GRID_SIZE
        lon_max = (lon_cell + 1) * LON_GRID_SIZE

        # Check if the cell overlaps with any pollution zone
        cell_in_zone = False

        for station, coords in monitoring_stations.items():
            if is_cell_in_pollution_zone(lat_min, lat_max, lon_min, lon_max, coords, 0.6):  # 0.6 km radius (increased)
                cell_in_zone = True
                break

        # If cell is in a pollution zone, color it based on tree count
        if cell_in_zone:
            tree_color = get_tree_color(tree_count, max_tree_count)
            folium.Rectangle(
                bounds=[[lat_min, lon_min], [lat_max, lon_max]],
                color=tree_color,
                fill=True,
                fill_opacity=0.5,
                popup=f'Trees: {tree_count}'
            ).add_to(belfast_map)
        else:
            # If not in the pollution zone, gray it out or remove it
            folium.Rectangle(
                bounds=[[lat_min, lon_min], [lat_max, lon_max]],
                color='white',
                fill=True,
                fill_opacity=0.0
            ).add_to(belfast_map)

    # Calculate and display average pollution for each pollution zone
    pollution_column_mapping = {
        'Belfast_Westlink': 'Belfast Westlink Roden Street',
        'Belfast_Stockmans_Lane': 'Belfast Stockmans Lane',
        'Belfast_Ormeau': 'Belfast Ormeau Road',
        'Belfast_Newtownards': 'Belfast Newtownards Road',
        'Belfast_Centre': 'Belfast Centre'
    }

    for station, coords in monitoring_stations.items():
        # Calculate the average pollution score
        file_key = station.replace(' ', '_')
        pollutant_col = pollution_column_mapping[file_key]
        avg_pollution = calculate_average_pollution(pollution_files[file_key], pollutant_col)

        # Add the pollution zone circle and display average pollution and station name
        folium.Circle(
            radius=600,  # Increased radius (600 meters)
            location=coords,
            popup=f'{station} - Avg Pollution: {avg_pollution:.2f} µg/m³',
            color='purple',
            fill=True,
            fill_color='purple',
            fill_opacity=0.3
        ).add_to(belfast_map)

    # Save the map to an HTML file
    map_path = 'belfast_tree_pollution_overlay_with_pollution_scores.html'
    belfast_map.save(map_path)

    return map_path
