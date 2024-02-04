#drone class for airsim
import airsim
import time
import asyncio
import numpy as np

class Drone:
    client = airsim.MultirotorClient()
    def __init__(self, x, y, z, DroneName = ""):
        self.client.enableApiControl(True, DroneName)
        self.client.armDisarm(True, DroneName)
        self.x = x
        self.y = y
        self.z = z
        self.client.takeoffAsync(vehicle_name=DroneName)
        #self.client.moveToPositionAsync(self.x, self.z, -self.y, 5).join()
        self.name = DroneName

    def update(self):
        self.x = self.client.simGetGroundTruthKinematics(vehicle_name=self.name).position.x_val
        self.y = self.client.simGetGroundTruthKinematics(vehicle_name=self.name).position.y_val
        self.z = self.client.simGetGroundTruthKinematics(vehicle_name=self.name).position.z_val
        print("Current location: (%f, %f, %f)" % (self.x, self.z, -self.y))
    async def move(self, x, y, z,velocity,delay = 0):
        try:
            x = float(x)
            y = float(y)
            z = float(z)
            velocity = float(velocity)
        except ValueError:
            print("Invalid input. Please enter a number.")
            return
        await asyncio.sleep(delay)
        x = float(x)
        y = float(y)
        z = float(z)

        self.client.moveToPositionAsync(x, z, -y, velocity,vehicle_name=self.name)
        #using self.client.simGetGroundTruthKinematics().position to get current location and cancellast task, check when drone is within 1m of target location
        while True:
            x_loc = self.client.simGetGroundTruthKinematics(vehicle_name=self.name).position.x_val
            y_loc = self.client.simGetGroundTruthKinematics(vehicle_name=self.name).position.y_val
            z_loc = self.client.simGetGroundTruthKinematics(vehicle_name=self.name).position.z_val
            location = np.array([x_loc, y_loc, z_loc])
            target = np.array([x, y, z])
            distance = np.linalg.norm(location - target)
            if distance < 1:
                self.client.cancelLastTask(vehicle_name=self.name)
                break


        self.update()
    def orbit(self,x,y,z,radius,orbits):
        try:
            x = float(x)
            y = float(y)
            z = float(z)
            radius = float(radius)
            orbits = int(orbits)
        except ValueError:
            return

        for i in range(orbits):
            self.client.moveToPositionAsync(x+radius, z, -y, 5).join()
            self.client.moveToPositionAsync(x, z+radius, -y, 5).join()
            self.client.moveToPositionAsync(x-radius, z, -y, 5).join()
            self.client.moveToPositionAsync(x, z-radius, -y, 5).join()
        self.update()

    #https: // github.com / Microsoft / AirSim / issues / 1677 -potential way to prevent overshoots