import folium
import pandas as pd
import numpy as np

# Load your tree data CSV file (update the path to the file location on your system)
tree_data = pd.read_csv(r'C:\Users\benmc\GitHub\hackathon\hackathon\odTrees.csv', low_memory=False)

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

# Filter out squares with 0 trees before finding the lowest density ones
non_zero_density_indices = np.where(tree_density_grid > 0)
non_zero_tree_density = tree_density_grid[non_zero_density_indices]

# Sort and find the indices of the top 10 lowest non-zero tree density squares
top_10_lowest_density_indices = np.argsort(non_zero_tree_density)[:10]
low_density_lat_idx, low_density_lon_idx = non_zero_density_indices[0][top_10_lowest_density_indices], \
non_zero_density_indices[1][top_10_lowest_density_indices]

# Add grid squares, tree density labels, and tree markers for the larger area, excluding 0-value squares
square_number = 1  # Initialize square numbering
total_trees = 0

for lat_idx in range(len(lat_edges_section) - 1):
    for lon_idx in range(len(lon_edges_section) - 1):
        # Skip squares with 0 trees
        if tree_density_grid[lat_idx, lon_idx] == 0:
            continue

        # Color the grid square
        color = 'blue'
        if (lat_idx, lon_idx) in zip(low_density_lat_idx, low_density_lon_idx):
            color = 'red'  # Mark the top 10 lowest-density squares in red

        # Add the grid square
        folium.Rectangle(
            bounds=[
                [lat_edges_section[lat_idx], lon_edges_section[lon_idx]],
                [lat_edges_section[lat_idx + 1], lon_edges_section[lon_idx + 1]],
            ],
            color=color,
            fill=True,
            fill_opacity=0.3 if color == 'red' else 0.1
        ).add_to(section_grid_map)

        # Calculate the number of trees in the current square
        num_trees_in_square = tree_density_grid[lat_idx, lon_idx]
        total_trees += num_trees_in_square

        # Add label showing the number of trees and square number
        folium.Marker(
            location=[(lat_edges_section[lat_idx] + lat_edges_section[lat_idx + 1]) / 2,
                      (lon_edges_section[lon_idx] + lon_edges_section[lon_idx + 1]) / 2],
            icon=folium.DivIcon(
                html=f'<div style="font-size: 10pt">#{square_number}: {int(num_trees_in_square)} trees</div>')
        ).add_to(section_grid_map)

        # Increment the square number
        square_number += 1

print(f"Total trees counted: {total_trees}")

# Save the map to an HTML file (update the path to your desired location)
section_grid_map.save(r'C:\Users\benmc\GitHub\hackathon\hackathon\belfast_greenery_map.html')
