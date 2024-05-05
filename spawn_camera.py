###################################################
# Spawn_camera.py
# Developer: Joshua Chang
# Date: 4/21/2024
# Description: This script will spawn a camera at specified locations and capture images
# On 'Purdue_airport3_7'
##################################################

import math
import airsim

def lat_long_to_local_xy(target_lat, target_long, origin_lat, origin_long, scale=1):
    """
    Convert latitude and longitude to local X, Y coordinates based on a reference origin.
    
    Parameters:
    - target_lat, target_long: Latitude and longitude of the target point.
    - origin_lat, origin_long: Latitude and longitude of the reference origin point.
    - scale: Scale factor for conversion to Unreal Engine units (default is 1).
    
    Returns:
    - Tuple (x, y) representing local coordinates in Unreal Engine environment.
    """
    # Earth's radius in meters
    R = 6378137
    
    # Convert latitude and longitude differences to radians
    delta_lat = math.radians(target_lat - origin_lat)
    delta_long = math.radians(target_long - origin_long)
    
    # Average latitude for the longitude calculation
    avg_lat = math.radians((origin_lat + target_lat) / 2.0)
    
    # Calculate X, Y distances in meters
    x_distance = R * delta_long * math.cos(avg_lat)
    y_distance = R * delta_lat
    
    # Apply scale if needed
    x = x_distance * scale
    y = y_distance * scale
    
    return x, y






def lat_long_to_local_xy_rotated(target_lat, target_long, origin_lat, origin_long, scale=1):
    """
    Adjusted to account for 90 degrees rotation: Positive Y is East, Positive X is North.
    
    Parameters:
    - target_lat, target_long: Latitude and longitude of the target point.
    - origin_lat, origin_long: Latitude and longitude of the reference origin point.
    - scale: Scale factor for conversion to Unreal Engine units (default is 1, considering rotation).
    
    Returns:
    - Tuple (x, y) representing local coordinates in Unreal Engine environment.
    """
    # Earth's radius in meters
    R = 6378137
    
    # Convert latitude and longitude differences to radians
    delta_lat = math.radians(target_lat - origin_lat)
    delta_long = math.radians(target_long - origin_long)
    
    # Average latitude for the longitude calculation
    avg_lat = math.radians((origin_lat + target_lat) / 2.0)
    
    # Adjust calculations for rotation: Latitude affects X, Longitude affects Y
    x_distance = R * delta_lat  # Now latitude difference affects X due to rotation
    y_distance = R * delta_long * math.cos(avg_lat)  # Longitude difference affects Y
    
    # Apply scale if needed, considering the rotation
    x = x_distance * scale
    y = y_distance * scale
    
    return x, y


# Example: Placing an object at specific geographic coordinates
# target_lat = 40.41575316846016  # jayanth algo target location
# target_long = -86.93270235873419  # 

target_lat = 40.414782578455885
target_long = -86.93324317088863

target_x = 30530
target_y = 11050

# Reference origin in Unreal Engine (replace with your actual origin)
origin_lat = 40.413000
origin_long = -86.934000

# Assume Unreal units match meters (scale=1)
scale = 277.6
# Now let's use the adjusted function with the scale that you found
scale = 100.5

x_rot, y_rot = lat_long_to_local_xy_rotated(target_lat, target_long, origin_lat, origin_long, scale)

# Calculate the error with the rotation considered
x_error_rot = x_rot - target_x
y_error_rot = y_rot - target_y

# Print the adjusted coordinates and errors
print(f"Adjusted for Rotation - Error in X, Y coordinates: {x_error_rot}, {y_error_rot}")
print('-----------------------------------')
print(f"Adjusted for Rotation - Calculated X, Y coordinates: {x_rot}, {y_rot}")
print(f"Target X, Y coordinates: {target_x}, {target_y}")


client = airsim.VehicleClient()
client.confirmConnection()

def list_scene_objects():
    # Connect to the AirSim simulator 


    # List all scene objects
    object_names = client.simListSceneObjects()
    asset_names = client.simListAssets()
    print("Available Objects in the Scene:")
    for name in object_names:
        print(name)
        
    print("\nAvailable Assets in the Scene:")
    for name in asset_names:
        print(name)

# Asset name of the blueprint object in the Unreal project database
# This should be the name of the asset as seen in Unreal's content browser
# asset_name = "Simple-cube"
asset_name = "Recording_camera5"
# Desired name for the new object instance
# object_name = "SimpleCubeInstance"
object_name = "RecordingCamera5Instance"
z_offset = -65  # Offset in centimeters to place the object above the ground

z_adjusted = 1000 + z_offset  # Adjusted z coordinate for Unreal units

yaw = math.radians(90)

# Coordinates and orientation for where you want to spawn the object
x, y, z = x_rot/100, y_rot/100, z_adjusted/100  # Example coordinates
# x, y, z = 13204/100, 28285/100, 0.0  # Example coordinates
# Spawn the blueprint object at the specified pose and scale
spawned_object_name = client.simSpawnObject(object_name=object_name, 
                                            asset_name=asset_name, 
                                            pose=airsim.Pose(airsim.Vector3r(x, y, -z), airsim.to_quaternion(0, 0, yaw)), 
                                            scale=airsim.Vector3r(1, 1, 1),
                                            is_blueprint=True)  # Indicate that this is a blueprint

if spawned_object_name:
    print(f"Successfully spawned '{spawned_object_name}' at the specified location.")
else:
    print("Failed to spawn the object. Please check the asset name and parameters.")
    
def create_vehicle(location, rotation, vehicle_name):
    # Create a vehicle at the specified location and rotation using simAddVehicle
    #Add new vehicle via RPC

    """
    Create vehicle at runtime
    simAddVehicle(self, vehicle_name, vehicle_type, pose, pawn_path = ""):
    Args:
        vehicle_name (str): Name of the vehicle being created
        vehicle_type (str): Type of vehicle, e.g. "simpleflight"
        pose (Pose): Initial pose of the vehicle
        pawn_path (str, optional): Vehicle blueprint path, default empty wbich uses the default blueprint for the vehicle type

    Returns:
        bool: Whether vehicle was created
    """
    client.simAddVehicle(vehicle_name, 'SimpleFlight', airsim.Pose(location, airsim.to_quaternion(0, 0, 0)), '')


    

vehicle_location_lat = 40.41431673902852
vehicle_location_long = -86.93362221272005
vehicle_yaw = math.radians(45)
vehicle_x, vehicle_y = lat_long_to_local_xy_rotated(vehicle_location_lat, vehicle_location_long, origin_lat, origin_long, scale)
vehicle_location = airsim.Vector3r(vehicle_x/100, vehicle_y/100, -z_offset/100)

create_vehicle(vehicle_name='drone2', location=vehicle_location, rotation=airsim.to_quaternion(0, 0, vehicle_yaw))