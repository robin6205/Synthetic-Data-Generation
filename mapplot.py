import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as patches

# Load the image
image_path = 'purduemapview2.png'
img = mpimg.imread(image_path)

# Initialize the plot
fig, ax = plt.subplots()

# Display the image with the origin set to 'lower' to flip the y-axis


# Set grid interval: change dx and dy to adjust the grid size
dx, dy = 50, 50

# Customize the grid
# ax.set_xticks([x for x in range(0, img.shape[1], dx)], minor=False)
# ax.set_yticks([y for y in range(0, img.shape[0], dy)], minor=False)
ax.grid(which='both', color='black', linestyle='-', linewidth=1)
ax.tick_params(axis='both', which='both', length=0)
# plt.xticks(rotation=90)

# Invert y-axis to move 0,0 to the bottom left
# ax.invert_yaxis()
# Define the vertices for building 1
building1_vertices = [
    (336.6, 259.3),  # Bottom left
    (335.8, 225.3),  # Top left
    (339, 224.5),    # Top right
    (339, 258.5)     # Bottom right
]

# # Create a Polygon patch
# building1_polygon = patches.Polygon(building1_vertices, closed=True, fill=False, edgecolor='red', linewidth=2)
# ax.add_patch(building1_polygon)
# Add interactive capabilities
# def format_coord(x, y):
#     # Flip the y-coordinate value
#     return 'x={}, y={}'.format(int(x), int(img.shape[0] - y))

# ax.format_coord = format_coord

#flip the order of y axis ticker
# plt.gca().invert_yaxis()
ax.imshow(img)

# Enable interactive mode
# plt.ion()

# Show the plot
plt.show()
