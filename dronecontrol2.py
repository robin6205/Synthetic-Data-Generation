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



#getting data from file or creating test data
#command_file = "C:/Users/LocalUser/Desktop/20230801-130000_200000.json" #CHANGE TO COMMAND FILE LOCATION
#commands = get_commands_list(command_file)
commands = {"test1":[(40.41580,-86.92763,100),(40.41565,-86.92513,100),(40.41477024709311, -86.93331139622599,20)]}
#print(commands)

#initialize drones
drone1 = Drone(0, 10, 0, "Drone1")
drone2 = Drone(0, 10, 0, "Drone2")
drone3 = Drone(0, 10, 0, "Drone3")
drone4 = Drone(0, 10, 0, "Drone4")
drone5 = Drone(0, 10, 0, "Drone5")

#run commands from file
async def run_commands(drone, commands):
    for step in commands[drone.name]:
        #print(step)
        time.sleep(.5)
        await drone.move(step["x"], step["y"], step["z"], step["velocity"], step["delay"])
async def run_commands_test(drone,commands):
    for step in commands["a8956e"]:
        print(step)
        await drone.movegps(step[0],step[1],step[2],20,0)
async def run_commands_test2(drone,commands):
    for step in commands["test1"]:
        print(step)
        await drone.movegps(step[0],step[1],step[2],17,0)


async def main():
    #initialize drone tasks
    drone_tasks = {drone1.name: None, drone2.name: None,drone3.name: None, drone4.name: None,drone5.name: None}
    drone_dict = {"1": drone1, "2": drone2, "3": drone3, "4": drone4, "5": drone5}
    session = PromptSession()
    #prompt user for command
    while True:
        user_command = await get_user_command(session,"Enter command (move, movegps, file, quit): ")

        if user_command == "quit":
            break

        if user_command == "file":
            drone_tasks[drone1.name] = asyncio.create_task(run_commands_test2(drone1, commands))
            await asyncio.gather(drone_tasks[drone1.name])
            '''drone_tasks[drone2.name] = asyncio.create_task(run_commands(drone2, commands))
            drone_tasks[drone3.name] = asyncio.create_task(run_commands(drone3, commands))
            drone_tasks[drone4.name] = asyncio.create_task(run_commands(drone4, commands))
            drone_tasks[drone5.name] = asyncio.create_task(run_commands(drone5, commands))
            await asyncio.gather(drone_tasks[drone1.name], drone_tasks[drone2.name],drone_tasks[drone3.name],
                                 drone_tasks[drone4.name],drone_tasks[drone5.name])'''
        #deprecated move command used in blocks environment
        if user_command == "move":
            user_input = await get_user_command(session,"Select a drone (1 or 2 or 3 or 4 or 5): ")
            drone_dict = {"1": drone1, "2": drone2, "3": drone3, "4": drone4, "5": drone5}
            selected_drone = drone_dict[user_input]
            if drone_tasks[selected_drone.name] and not drone_tasks[selected_drone.name].done():
                print(f"{selected_drone.name} is still executing a task. Please wait for it  o finish.")
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

        #gps movement commands
        if user_command == "movegps":
            user_input = await get_user_command(session,"Select a drone (1 or 2 or 3 or 4 or 5): ")
            drone_dict = {"1": drone1, "2": drone2, "3": drone3, "4": drone4, "5": drone5}
            selected_drone = drone_dict[user_input]
            if drone_tasks[selected_drone.name] and not drone_tasks[selected_drone.name].done():
                print(f"{selected_drone.name} is still executing a task. Please wait for it to finish.")
                continue
            latitude = float(await get_user_command(session,"Enter latitude: "))
            longitude = float(await get_user_command(session,"Enter longitude: "))
            altitude = float(await get_user_command(session,"Enter altitude: "))
            velocity = float(await get_user_command(session,"Enter desired velocity: "))
            if velocity <= 0:
                print("Velocity must be a positive number")
                continue
            delay = float(await get_user_command(session,"Enter desired delay: "))
            drone_tasks[selected_drone.name] = asyncio.create_task(selected_drone.movegps(latitude, longitude, altitude, velocity, delay))
        await asyncio.sleep(0)  # Give time for other tasks to run





if __name__ == "__main__":
    asyncio.run(main())


