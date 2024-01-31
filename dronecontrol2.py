import airsim
import time
from drone import Drone
import os
from extractjson import get_commands_list
import asyncio

#connect to server with drone controls
Drone.client = airsim.MultirotorClient()
Drone.client.enableApiControl(True, "Drone1")
Drone.client.enableApiControl(True, "Drone2")
Drone.client.armDisarm(True, "Drone1")
Drone.client.armDisarm(True, "Drone2")
f1 = client.takeoffAsync(vehicle_name="Drone1")
f2 = client.takeoffAsync(vehicle_name="Drone2")
f1.join()
f2.join()
command_file = "C:/Users/aleca/Desktop/test2.json"
commands = get_commands_list(command_file)
print(commands)
drones = ["Drone1","Drone2"]
print("a")
for drone in drones:
    for command in commands[drone]:
        client.moveToPositionAsync(command["x"], command["z"], -command["y"], 5, vehicle_name=drone)




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
