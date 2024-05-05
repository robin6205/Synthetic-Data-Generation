import airsim
import json

# Function to read coordinates from the 'sim_coords2.json' file
def read_coordinates_from_json(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        path_coordinates = data.get('path', [])
    return path_coordinates

# Main function to move drone based on GPS coordinates
def move_drone_to_gps_location(latitude, longitude, altitude, velocity):
    # Connect to the AirSim simulator as a MultirotorClient
    client = airsim.MultirotorClient()
    client.confirmConnection()
    client.enableApiControl(True)
    client.armDisarm(True)
    # client.setVelocityControllerGains(airsim.VelocityControllerGains(z_gains=airsim.PIDGains(0.1, 0, 0)))

    # Take off and hover to ensure the drone is airborne
    print("Taking off...")
    client.takeoffAsync().join()

    # Read coordinates from the JSON file
    path_coordinates = read_coordinates_from_json('sim_coords2.json')

    # Move to each GPS location in the path
    for coord in path_coordinates:
        latitude, longitude = coord  # Assuming each coordinate is [lat, long]
        print(f"Moving to GPS location: Latitude={latitude}, Longitude={longitude}, Altitude={altitude} at {velocity} m/s")
        client.moveToGPSAsync(latitude=latitude, longitude=longitude, altitude=altitude, velocity=velocity).join()

    # Ensure safe landing after reaching the last destination
    print("Landing...")
    client.landAsync().join()

    # Cleanup by disarming and releasing API control
    client.armDisarm(False)
    client.enableApiControl(False)

# Specify the desired altitude and velocity
altitude = 130
velocity = 15  # Desired velocity in meters per second

# Call the function with your desired starting latitude and longitude
move_drone_to_gps_location(latitude=40.41508599719736, longitude=-86.93484426930432, altitude=altitude, velocity=velocity)
