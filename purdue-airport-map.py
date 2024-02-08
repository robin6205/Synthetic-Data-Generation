import folium

# Define the coordinates
upper_left_lat, upper_left_lon = 40.420210, -86.958496
bottom_right_lat, bottom_right_lon = 40.403734, -86.921700

# Center of the area for initializing the map
center_lat = (upper_left_lat + bottom_right_lat) / 2
center_lon = (upper_left_lon + bottom_right_lon) / 2

# Create a folium map with a satellite view
map = folium.Map(location=[center_lat, center_lon], zoom_start=14)

# Add the satellite tile layer with attribution
folium.TileLayer('Stamen Terrain', attr='Map data © OpenStreetMap contributors').add_to(map)

# Function to create a square grid overlay
def create_grid(upper_left, bottom_right, n=100):
    lat_steps = (upper_left[0] - bottom_right[0]) / n
    lon_steps = (bottom_right[1] - upper_left[1]) / n

    for i in range(n):
        for j in range(n):
            nw = (upper_left[0] - i * lat_steps, upper_left[1] + j * lon_steps)
            se = (nw[0] - lat_steps, nw[1] + lon_steps)
            folium.Rectangle(
                bounds=[nw, se],
                color='blue',
                fill=True,
                fill_opacity=0.2,
                # line opcity set to 0.2
                opacity=0.2
            ).add_to(map)

# Add the grid to the map
create_grid((upper_left_lat, upper_left_lon), (bottom_right_lat, bottom_right_lon))

# Save the map to an HTML file
map.save('interactive_map_with_voxels.html')