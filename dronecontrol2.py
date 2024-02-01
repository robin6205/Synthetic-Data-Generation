import airsim
import time
from drone import Drone
import os
from extractjson import get_commands_list
import asyncio
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout

async def get_user_command(session):
    with patch_stdout():
        return await session.prompt_async("Enter command (move, file, quit): ")




command_file = "C:/Users/aleca/Desktop/test2.json"
commands = get_commands_list(command_file)
print(commands)
drone1 = Drone(0, 10, 0, "Drone1")
drone2 = Drone(0, 10, 0, "Drone2")

async def run_commands(drone, commands):
    for step in commands[drone.name]:
        await drone.move(step["x"], step["y"], step["z"], step["velocity"], step["delay"])


async def main():
    drone_tasks = {drone1.name: None, drone2.name: None}

    while True:
        session = PromptSession()

        user_command = await get_user_command(session)

        if user_command == "quit":
            break

        if user_command == "file":
            drone_tasks[drone1.name] = asyncio.create_task(run_commands(drone1, commands))
            drone_tasks[drone2.name] = asyncio.create_task(run_commands(drone2, commands))
            await asyncio.gather(drone_tasks[drone1.name], drone_tasks[drone2.name])
        if user_command == "move":
            user_input = input("Select a drone (1 or 2): ")
            selected_drone = drone1 if user_input == "1" else drone2
            if drone_tasks[selected_drone.name] and not drone_tasks[selected_drone.name].done():
                print(f"{selected_drone.name} is still executing a task. Please wait for it to finish.")
                continue
            x = float(input("Enter desired x-coordinate: "))
            y = float(input("Enter desired y-coordinate: "))
            z = float(input("Enter desired z-coordinate: "))
            velocity = float(input("Enter desired velocity: "))
            delay = float(input("Enter desired delay: "))
            drone_tasks[selected_drone.name] = asyncio.create_task(selected_drone.move(x, y, z, velocity, delay))
        await asyncio.sleep(0.1)  # Give time for other tasks to run





if __name__ == "__main__":
    asyncio.run(main())



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
