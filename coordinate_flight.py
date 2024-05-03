import airsim
import time
import json

import airsim

# Main function to move drone based on GPS coordinates
def move_drone_to_gps_location(latitude, longitude, altitude, velocity):
    # Connect to the AirSim simulator as a MultirotorClient
    client = airsim.MultirotorClient()
    client.confirmConnection()
    client.enableApiControl(True)
    client.armDisarm(True)

    # Take off and hover to ensure the drone is airborne
    print("Taking off...")
    client.takeoffAsync().join()
    
    # first fly up to 30 meters
    # print("Flying up...")
    # client.moveToPositionAsync(0, 0, -10, 5).join()

    print(f"Moving to GPS location: Latitude={latitude}, Longitude={longitude}, Altitude={altitude} at {velocity} m/s")
    
    #get current gps altitude
    gps = client.getGpsData()
    print("Current GPS altitude: ", gps)
    
    # Move to the specified GPS location
    client.moveToGPSAsync(latitude = latitude, longitude = longitude, altitude = altitude, velocity = velocity).join()

    # Ensure safe landing after reaching the destination
    print("Landing...")
    client.landAsync().join()

    # Cleanup by disarming and releasing API control
    client.armDisarm(False)
    client.enableApiControl(False)

# Specify the GPS coordinates you want the drone to navigate to
# latitude = 40.41356425186632
# longitude = -86.93421822607813
latitude = 40.41508599719736
longitude = -86.93484426930432

#print current altitude and set the altitude
# set to current altitude + 10 meters
altitude = 200
velocity = 5  # Desired velocity in meters per second


# client = airsim.MultirotorClient()
# client.confirmConnection()
# client.enableApiControl(True)
# print("Arming the drone...")
# client.armDisarm(True)


# Call the function with the specified GPS coordinates
move_drone_to_gps_location(latitude, longitude, altitude, velocity)
