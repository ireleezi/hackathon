import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Load datasets with proper encoding and handling mixed types
trees_df = pd.read_csv(r'C:\Users\benmc\GitHub\hackathon\hackathon\odTrees.csv', low_memory=False)

print(trees_df.columns)

# Handle possible encoding issues in air pollution datasets
pollution_dfs = {
    'Ormeau': pd.read_csv(r'C:\Users\benmc\GitHub\hackathon\hackathon\ormeauAirPollution.csv', encoding='ISO-8859-1'),
    'Belfast Centre': pd.read_csv(r'C:\Users\benmc\GitHub\hackathon\hackathon\belfastCentreAirPollution.csv', encoding='ISO-8859-1'),
    'Westlink': pd.read_csv(r'C:\Users\benmc\GitHub\hackathon\hackathon\westlinkAirPollution.csv', encoding='ISO-8859-1'),
    'Stockmans': pd.read_csv(r'C:\Users\benmc\GitHub\hackathon\hackathon\stockmansAirPollution.csv', encoding='ISO-8859-1'),
    'Newtownards': pd.read_csv(r'C:\Users\benmc\GitHub\hackathon\hackathon\newtownardsAirPollution.csv', encoding='ISO-8859-1')
}

# Combine pollution datasets into a single DataFrame
pollution_df = pd.concat(pollution_dfs.values(), ignore_index=True)

# Function to generate a 1km square grid for Belfast
def generate_grid(min_x, max_x, min_y, max_y, grid_size=1.0):
    x_coords = np.arange(min_x, max_x, grid_size)
    y_coords = np.arange(min_y, max_y, grid_size)
    grid = [(x, y) for x in x_coords for y in y_coords]
    return pd.DataFrame(grid, columns=['x', 'y'])

# Create grid (adjust min/max coordinates based on your data)
# Use 'TREELOCATIONX' and 'TREELOCATIONY' or 'LONGITUDE' and 'LATITUDE' for grid coordinates
min_x, max_x = trees_df['TREELOCATIONX'].min(), trees_df['TREELOCATIONX'].max()
min_y, max_y = trees_df['TREELOCATIONY'].min(), trees_df['TREELOCATIONY'].max()

# If you're using 'LONGITUDE' and 'LATITUDE' for geospatial data:
# min_x, max_x = trees_df['LONGITUDE'].min(), trees_df['LONGITUDE'].max()
# min_y, max_y = trees_df['LATITUDE'].min(), trees_df['LATITUDE'].max()

grid_df = generate_grid(min_x, max_x, min_y, max_y)

# Assign pollution data to grid squares based on proximity
def assign_pollution_to_grid(pollution_df, grid_df, grid_size=1.0):
    pollution_grid = []
    for _, row in grid_df.iterrows():
        grid_x, grid_y = row['x'], row['y']
        # Calculate the center point of the grid square
        center_x, center_y = grid_x + grid_size / 2, grid_y + grid_size / 2
        # Find the nearest pollution measurement
        pollution_row = pollution_df.iloc[((pollution_df['x'] - center_x)**2 + (pollution_df['y'] - center_y)**2).idxmin()]
        pollution_grid.append(pollution_row['pollution_level'])  # Adjust based on pollution data format
    grid_df['pollution'] = pollution_grid
    return grid_df

# Assign pollution data to grid
grid_df = assign_pollution_to_grid(pollution_df, grid_df)

# Add tree density to grid
def assign_tree_density_to_grid(trees_df, grid_df, grid_size=1.0):
    tree_density = []
    for _, row in grid_df.iterrows():
        grid_x, grid_y = row['x'], row['y']
        # Count trees within each grid square
        trees_in_grid = trees_df[(trees_df['x'] >= grid_x) & (trees_df['x'] < grid_x + grid_size) &
                                 (trees_df['y'] >= grid_y) & (trees_df['y'] < grid_y + grid_size)]
        tree_density.append(len(trees_in_grid))
    grid_df['tree_density'] = tree_density
    return grid_df

# Assign tree density
grid_df = assign_tree_density_to_grid(trees_df, grid_df)

# Normalize data for machine learning
scaler = StandardScaler()
grid_df[['pollution', 'tree_density']] = scaler.fit_transform(grid_df[['pollution', 'tree_density']])

# Use KMeans clustering to identify the 5 areas with the highest need for trees
def recommend_tree_planting_areas(grid_df, num_clusters=5):
    kmeans = KMeans(n_clusters=num_clusters)
    grid_df['cluster'] = kmeans.fit_predict(grid_df[['pollution', 'tree_density']])
    return grid_df.sort_values(by='pollution', ascending=False).head(num_clusters)

# Recommend 5 areas for tree planting
recommended_areas = recommend_tree_planting_areas(grid_df)

# Visualization of the grid with pollution and tree density
def plot_grid(grid_df):
    fig, ax = plt.subplots(figsize=(10, 10))
    sc = ax.scatter(grid_df['x'], grid_df['y'], c=grid_df['pollution'], cmap='RdYlGn', s=100, alpha=0.5)
    ax.set_title('Tree Density and Pollution Levels in Belfast')
    plt.colorbar(sc, label='Pollution Level')
    for _, row in grid_df.iterrows():
        ax.text(row['x'], row['y'], f'T: {int(row["tree_density"])}', fontsize=8, ha='center')
    plt.show()

# Plot the grid
plot_grid(grid_df)

# Output the recommended areas
print(recommended_areas[['x', 'y', 'pollution', 'tree_density']])
