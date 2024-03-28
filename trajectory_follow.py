import airsim
import time
import json



# Function to read waypoints from the JSON file
def read_waypoints(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data["Trajectory"]["Blocks_env"]



def navigate(client, waypoints):
    # Navigate through waypoints
    for point in waypoints:
        x, y, z = point["X"], point["Y"], point["Z"]
        heading = point["Heading"]
        # speed = point["Speed"]]
        speed = point["Speed"]
        print(f"Moving to (X: {y}, Y: {x}, Z: {z}) at speed {speed} m/s")
        client.moveToPositionAsync(y, x, z, speed).join()
        # Optional: Adjust the drone's heading
        # client.rotateToYawAsync(heading).join()

#print current position
# position = client.simGetVehiclePose().position
# print("Current position: ", position)
# Connect to the AirSim simulator 
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)

# Read waypoints from the JSON file
# waypoints = read_waypoints("airport_trajectory.json")

# Navigate through waypoints
# navigate(client, waypoints)
# Arm the drone
print("Arming the drone...")
client.armDisarm(True)

# get current position
originalposition = client.simGetVehiclePose().position

# Take off
print("Taking off...")
client.takeoffAsync().join()

# fly forward for 10 meters


# print("Flying forward...to the first point")
# client.moveToPositionAsync(-70, 0, -1, 5).join()
# print("Flying forward... to the second point")
# client.moveToPositionAsync(-200, 0, -40, 10).join()
 
 
# fly up to 10 meter altitude 
print("Flying up...")
client.moveToPositionAsync(originalposition.x_val, originalposition.y_val, -15, 5).join()

time.sleep(50)

 


# Ensure safe landing
print("Landing...")
client.landAsync().join()
client.reset()
# Disarm and reset API control
client.armDisarm(False)