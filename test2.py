import airsim
import time
import drone
import os
from extractjson import get_commands_list

#connect to server with drone controls
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)
drone_controls = airsim.MultirotorClient()
command_file = "C:/Users/aleca/Desktop/test2.json"
commands = get_commands_list(command_file)
print(commands)


drone_one = drone.Drone(client, 0, 10, 0)

for step in commands["id1"]:
    time.sleep(step["delay"])
    drone_one.move(step["x"], step["y"], step["z"], step["velocity"])




'''while True:
    #print current location to console
    print(client.simGetGroundTruthKinematics().position)
    #ask user for command: move, orbit, or exit
    command = input("Enter command: ")
    if command == "move":
        x = input("Enter desired x-coordinate: ")
        y = input("Enter desired y-coordinate: ")
        z = input("Enter desired z-coordinate: ")
        drone_one.move(x,y,z)
    elif command == "orbit":
        x = input("Enter desired x-coordinate: ")
        y = input("Enter desired y-coordinate: ")
        z = input("Enter desired z-coordinate: ")
        radius = input("Enter desired radius: ")
        orbits = input("Enter desired number of orbits: ")
        drone_one.orbit(x,y,z,radius,orbits)
    elif command == "exit":
        break'''