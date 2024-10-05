import folium
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

# Load your tree data CSV file
tree_data = pd.read_csv(r'C:\Users\benmc\GitHub\hackathon\hackathon\odTrees.csv', low_memory=False)

# Load your air quality data CSV file
air_quality_data = pd.read_csv(r'C:\Users\benmc\GitHub\hackathon\hackathon\air_quality.csv', low_memory=False)

# Define the boundaries (with a small buffer to ensure all trees are included)
lat_min_section = 54.53  # Slightly reduced min latitude
lat_max_section = 54.67  # Slightly increased max latitude
lon_min_section = -6.00  # Slightly reduced min longitude
lon_max_section = -5.81  # Slightly increased max longitude

# Grid step size in degrees, approximately 1km x 1km
km_per_degree_lat = 111
km_per_degree_lon = 111 * np.cos(np.radians((lat_min_section + lat_max_section) / 2))
lat_step = 1 / km_per_degree_lat
lon_step = 1 / km_per_degree_lon

# Create latitude and longitude grid edges based on the larger section
lat_edges_section = np.arange(lat_min_section, lat_max_section, lat_step)
lon_edges_section = np.arange(lon_min_section, lon_max_section, lon_step)

# Initialize a map for the larger section of Belfast
section_grid_map = folium.Map(
    location=[(lat_min_section + lat_max_section) / 2, (lon_min_section + lon_max_section) / 2], zoom_start=13)

# Create a 2D array to store the tree count for each square
tree_density_grid = np.zeros((len(lat_edges_section) - 1, len(lon_edges_section) - 1))

# Initialize counter for excluded trees
excluded_trees = 0

# Loop through the tree data and populate the tree density grid
for index, row in tree_data.iterrows():
    lat_idx = np.searchsorted(lat_edges_section, row['LATITUDE'], side='right') - 1
    lon_idx = np.searchsorted(lon_edges_section, row['LONGITUDE'], side='right') - 1

    if 0 <= lat_idx < tree_density_grid.shape[0] and 0 <= lon_idx < tree_density_grid.shape[1]:
        tree_density_grid[lat_idx, lon_idx] += 1
    else:
        excluded_trees += 1

# Output number of trees that were excluded
print(f"Excluded trees: {excluded_trees}")

# Integrate air quality data (assuming air quality data has latitude and longitude)
air_quality_grid = np.zeros_like(tree_density_grid)

for index, row in air_quality_data.iterrows():
    lat_idx = np.searchsorted(lat_edges_section, row['LATITUDE'], side='right') - 1
    lon_idx = np.searchsorted(lon_edges_section, row['LONGITUDE'], side='right') - 1

    if 0 <= lat_idx < air_quality_grid.shape[0] and 0 <= lon_idx < air_quality_grid.shape[1]:
        air_quality_grid[lat_idx, lon_idx] += row['Nitrogen_Dioxide']  # Replace with relevant air pollutant column

# Prepare data for machine learning (tree density and air pollution)
combined_data = pd.DataFrame({
    'Tree Density': tree_density_grid.flatten(),
    'Air Pollution': air_quality_grid.flatten()
})

# Remove zero-value rows (areas with no trees and no air pollution)
combined_data = combined_data[(combined_data['Tree Density'] > 0) | (combined_data['Air Pollution'] > 0)]

# Apply K-means clustering to find areas for planting (5 clusters for demonstration)
kmeans = KMeans(n_clusters=5, random_state=42)
combined_data['Cluster'] = kmeans.fit_predict(combined_data[['Tree Density', 'Air Pollution']])

# Get the cluster with low tree density and high pollution (for planting recommendations)
cluster_centers = kmeans.cluster_centers_
recommended_cluster = np.argmin(cluster_centers[:, 0] / cluster_centers[:, 1])  # Low trees, high pollution

# Visualize the clusters on the map
for lat_idx in range(len(lat_edges_section) - 1):
    for lon_idx in range(len(lon_edges_section) - 1):
        tree_density = tree_density_grid[lat_idx, lon_idx]
        air_pollution = air_quality_grid[lat_idx, lon_idx]

        # Skip squares with 0 trees and 0 air pollution
        if tree_density == 0 and air_pollution == 0:
            continue

        # Determine the color based on the cluster
        cluster = combined_data.loc[(combined_data['Tree Density'] == tree_density) & (combined_data['Air Pollution'] == air_pollution), 'Cluster'].values[0]
        color = 'red' if cluster == recommended_cluster else 'blue'

        # Add the grid square to the map
        folium.Rectangle(
            bounds=[
                [lat_edges_section[lat_idx], lon_edges_section[lon_idx]],
                [lat_edges_section[lat_idx + 1], lon_edges_section[lon_idx + 1]],
            ],
            color=color,
            fill=True,
            fill_opacity=0.3 if color == 'red' else 0.1
        ).add_to(section_grid_map)

        # Add label showing tree density and air pollution
        folium.Marker(
            location=[(lat_edges_section[lat_idx] + lat_edges_section[lat_idx + 1]) / 2,
                      (lon_edges_section[lon_idx] + lon_edges_section[lon_idx + 1]) / 2],
            icon=folium.DivIcon(
                html=f'<div style="font-size: 10pt">Trees: {int(tree_density)}, NO2: {air_pollution:.2f}</div>')
        ).add_to(section_grid_map)

# Save the map to an HTML file (update the path to your desired location)
section_grid_map.save(r'C:\Users\benmc\GitHub\hackathon\hackathon\belfast_greenery_map_with_machine_learning.html')
