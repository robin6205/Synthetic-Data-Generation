from PIL import Image, ImageDraw, ImageEnhance
import math

# Open the image
image_path = "PurdueAirportMaps.png"
image = Image.open(image_path).convert("RGBA")

# Define the grid parameters
grid_spacing = 50  # Distance between grid lines in pixels

# Get image dimensions
width, height = image.size

# Create a new image for drawing the grid and arrows
overlay = Image.new("RGBA", image.size, (255, 255, 255, 0))
draw = ImageDraw.Draw(overlay)

# Draw vertical grid lines in grey
for x in range(0, width, grid_spacing):
    draw.line([(x, 0), (x, height)], fill=(128, 128, 128, 255), width=1)  # Grey color, 1 pixel width

# Draw horizontal grid lines in grey
for y in range(0, height, grid_spacing):
    draw.line([(0, y), (width, y)], fill=(128, 128, 128, 255), width=1)  # Grey color, 1 pixel width

# Function to draw an arrow
def draw_arrow(draw, start, end, color=(0, 0, 255, 255), arrowhead_length=10, arrowhead_angle=45):
    draw.line([start, end], fill=color, width=2)
    # Calculate arrowhead points
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    left_arrow_angle = angle + math.radians(arrowhead_angle)
    right_arrow_angle = angle - math.radians(arrowhead_angle)
    left_arrow = (end[0] - arrowhead_length * math.cos(left_arrow_angle), 
                  end[1] - arrowhead_length * math.sin(left_arrow_angle))
    right_arrow = (end[0] - arrowhead_length * math.cos(right_arrow_angle), 
                   end[1] - arrowhead_length * math.sin(right_arrow_angle))
    draw.line([end, left_arrow], fill=color, width=2)
    draw.line([end, right_arrow], fill=color, width=2)



# Function to draw a transparent red isosceles triangle with a red border
def draw_triangle(draw, bottom_right, side_length, fill_color=(255, 0, 0, 40), outline_color=(255, 0, 0, 255)):
    half_height = (math.sqrt(3) / 2) * side_length
    half_base = side_length / 2
    top_vertex = (bottom_right[0] - half_base, bottom_right[1] - half_height)
    left_vertex = (bottom_right[0] - side_length, bottom_right[1])
    draw.polygon([bottom_right, left_vertex, top_vertex], fill=fill_color, outline=outline_color)

# Function to draw a green circle
def draw_circle(draw, center, radius, color=(0, 255, 0, 255)):
    bbox = [center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius]
    draw.ellipse(bbox, fill=color)

# Define the triangle parameters
side_length = 1.5 * grid_spacing  # Adjust the side length as needed
triangle_corners = [(11,3.2),(10,3.2),(9,3),(8,2.7),(7,2.7),(6,2.5),(5,2.3),(4,2.3), (3, 2), (2,1.7), (1, 1.6)]  # Bottom right corners of triangles

# Draw triangles and green circles
for corner_index in triangle_corners:
    bottom_right_point = (corner_index[0] * grid_spacing, corner_index[1] * grid_spacing)
    draw_triangle(draw, bottom_right_point, side_length)
    draw_circle(draw, bottom_right_point, 5)  # Radius of 5 pixels
    
# Draw a blue arrow from grid (0,1) to (12,3)
start_index = (0, 1.2)
end_index = (12, 3.2)
start_point = (start_index[0] * grid_spacing, start_index[1] * grid_spacing)
end_point = (end_index[0] * grid_spacing, end_index[1] * grid_spacing)
draw_arrow(draw, start_point, end_point, color=(0, 0, 255, 255))

# Composite the overlay with the original image
combined = Image.alpha_composite(image, overlay)

# Save the new image with the grid, arrow, triangles, and circles
output_path = "PurdueAirportMaps_with_grid_arrow_triangles_circles.png"
combined.save(output_path)

# Display the image
combined.show()
