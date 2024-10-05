import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

##TODO Code needs to show the grid with each sqaures tree density and air pollution. Using all the combined datasets it needs to do some type of meddeling to decide where trees/greenery needs to go

# Load the tree dataset
trees_df = pd.read_csv('odTrees.csv', low_memory=False)

# Load the pollution datasets
pollution_dfs = {
    'Ormeau': pd.read_csv('ormeauAirPollution.csv', encoding='ISO-8859-1'),
    'Belfast Centre': pd.read_csv('belfastCentreAirPollution.csv', encoding='ISO-8859-1'),
    'Westlink': pd.read_csv('westlinkAirPollution.csv', encoding='ISO-8859-1'),
    'Stockmans': pd.read_csv('stockmansAirPollution.csv', encoding='ISO-8859-1'),
    'Newtownards': pd.read_csv('newtownardsAirPollution.csv', encoding='ISO-8859-1')
}


# Clean each dataset by renaming and removing unnecessary columns
def clean_pollution_data(df, columns_to_keep, new_column_names):
    df_cleaned = df[columns_to_keep]
    df_cleaned.columns = new_column_names
    return df_cleaned


# Clean the datasets (applying to each dataset individually)
cleanedData = clean_pollution_data(pollution_dfs['Newtownards'],
                                           ['ï»¿Belfast Newtownards Road', 'Unnamed: 1', 'Unnamed: 10'],
                                           ['Pollutant', 'Status', 'Temperature'])

# Print cleaned data to inspect
print("Cleaned Newtownards Dataset:\n", cleanedData.head())


# Repeat similar cleaning for other datasets (adjust column names for each)

# Create a grid for Belfast
def generate_grid(min_x, max_x, min_y, max_y, grid_size=1.0):
    x_coords = np.arange(min_x, max_x, grid_size)
    y_coords = np.arange(min_y, max_y, grid_size)
    grid = [(x, y) for x in x_coords for y in y_coords]
    return pd.DataFrame(grid, columns=['x', 'y'])


# Assuming the tree data provides x/y coordinates
min_x, max_x = trees_df['TREELOCATIONX'].min(), trees_df['TREELOCATIONX'].max()
min_y, max_y = trees_df['TREELOCATIONY'].min(), trees_df['TREELOCATIONY'].max()
grid_df = generate_grid(min_x, max_x, min_y, max_y)


# Assign tree density to the grid
def assign_tree_density_to_grid(trees_df, grid_df, grid_size=1.0):
    tree_density = []
    for _, row in grid_df.iterrows():
        grid_x, grid_y = row['x'], row['y']
        trees_in_grid = trees_df[
            (trees_df['TREELOCATIONX'] >= grid_x) & (trees_df['TREELOCATIONX'] < grid_x + grid_size) &
            (trees_df['TREELOCATIONY'] >= grid_y) & (trees_df['TREELOCATIONY'] < grid_y + grid_size)]
        tree_density.append(len(trees_in_grid))
    grid_df['tree_density'] = tree_density
    return grid_df


grid_df = assign_tree_density_to_grid(trees_df, grid_df)


# Function to assign pollution data by region (example with Newtownards)
def assign_pollution_by_region(region_name, region_data, grid_df):
    grid_df['region'] = region_name  # Assign region placeholder
    grid_df.loc[grid_df['region'] == region_name, 'pollution'] = region_data['Status'].str.extract('(\d+)').astype(
        float).mean()  # Example: extract numeric pollution data
    return grid_df


# Example usage: Assign pollution data for 'Belfast Newtownards Road'
grid_df = assign_pollution_by_region('Belfast Newtownards Road', cleanedData, grid_df)


# Repeat this step for other datasets/regions (Ormeau, Westlink, etc.)

# Machine Learning: KMeans to recommend tree planting areas
def recommend_tree_planting_areas(grid_df, num_clusters=5):
    # Normalize pollution and tree density for KMeans clustering
    scaler = StandardScaler()
    grid_df[['pollution', 'tree_density']] = scaler.fit_transform(grid_df[['pollution', 'tree_density']])

    kmeans = KMeans(n_clusters=num_clusters)
    grid_df['cluster'] = kmeans.fit_predict(grid_df[['pollution', 'tree_density']])

    # Select top 5 areas based on high pollution and low tree density
    return grid_df.sort_values(by='pollution', ascending=False).head(num_clusters)


# Recommend 5 areas for tree planting
recommended_areas = recommend_tree_planting_areas(grid_df)


# Visualization: Plot grid with tree density and pollution levels
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

# Output the recommended areas for tree planting
print("Recommended areas for tree planting:\n", recommended_areas[['x', 'y', 'pollution', 'tree_density']])


