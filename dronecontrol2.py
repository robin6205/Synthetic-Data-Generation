import airsim
import time
from drone import Drone
import os
from extractjson import get_commands_list
import asyncio
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout

async def get_user_command(session,prompt):
    with patch_stdout():
        return await session.prompt_async(prompt)




command_file = "C:/Users/aleca/Desktop/test2.json"
commands = get_commands_list(command_file)
#print(commands)
drone1 = Drone(0, 10, 0, "Drone1")
drone2 = Drone(0, 10, 0, "Drone2")
drone3 = Drone(0, 10, 0, "Drone3")
drone4 = Drone(0, 10, 0, "Drone4")
drone5 = Drone(0, 10, 0, "Drone5")


async def run_commands(drone, commands):
    for step in commands[drone.name]:
        print(step)
        await drone.move(step["x"], step["y"], step["z"], step["velocity"], step["delay"])


async def main():
    drone_tasks = {drone1.name: None, drone2.name: None,drone3.name: None, drone4.name: None,drone5.name: None}
    drone_dict = {"1": drone1, "2": drone2, "3": drone3, "4": drone4, "5": drone5}
    session = PromptSession()

    while True:
        user_command = await get_user_command(session,"Enter command (move, file, quit): ")

        if user_command == "quit":
            break

        if user_command == "file":
            drone_tasks[drone1.name] = asyncio.create_task(run_commands(drone1, commands))
            #await asyncio.gather(drone_tasks[drone1.name])
            drone_tasks[drone2.name] = asyncio.create_task(run_commands(drone2, commands))
            drone_tasks[drone3.name] = asyncio.create_task(run_commands(drone3, commands))
            drone_tasks[drone4.name] = asyncio.create_task(run_commands(drone4, commands))
            drone_tasks[drone5.name] = asyncio.create_task(run_commands(drone5, commands))
            await asyncio.gather(drone_tasks[drone1.name], drone_tasks[drone2.name],drone_tasks[drone3.name],
                                 drone_tasks[drone4.name],drone_tasks[drone5.name])
        if user_command == "move":
            user_input = await get_user_command(session,"Select a drone (1 or 2 or 3 or 4 or 5): ")
            drone_dict = {"1": drone1, "2": drone2, "3": drone3, "4": drone4, "5": drone5}
            selected_drone = drone_dict[user_input]
            if drone_tasks[selected_drone.name] and not drone_tasks[selected_drone.name].done():
                print(f"{selected_drone.name} is still executing a task. Please wait for it to finish.")
                continue
            x = float(await get_user_command(session,"Enter desired x-coordinate: "))
            y = float(await get_user_command(session,"Enter desired y-coordinate: "))
            z = float(await get_user_command(session,"Enter desired z-coordinate: "))
            velocity = float(await get_user_command(session,"Enter desired velocity: "))
            if velocity <= 0:
                print("Velocity must be a positive number")
                continue
            delay = float(await get_user_command(session,"Enter desired delay: "))
            drone_tasks[selected_drone.name] = asyncio.create_task(selected_drone.move(x, y, z, velocity, delay))
        await asyncio.sleep(0)  # Give time for other tasks to run





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
