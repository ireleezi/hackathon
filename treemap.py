import folium

# Create a map centered around the average latitude and longitude in the dataset
center_lat = data['LATITUDE'].mean()
center_lon = data['LONGITUDE'].mean()

# Create a Folium map centered on Belfast
m = folium.Map(location=[center_lat, center_lon], zoom_start=12)

# Add tree locations to the map
for i, row in data.iterrows():
    folium.CircleMarker(
        location=[row['LATITUDE'], row['LONGITUDE']],
        radius=3,
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.6,
        popup=f"Species: {row['SPECIESTYPE']}\nHeight: {row['TREEHEIGHTinMETRES']} m"
    ).add_to(m)

# Save the map to an HTML file to view it
map_file_path = '/mnt/data/belfast_trees_map.html'
m.save(map_file_path)

map_file_path  # Return the file path for the map
