#drone class for airsim
import airsim
import time
import asyncio
import numpy as np


async def await_airsim_future(future):
    while not future.is_done():
        await asyncio.sleep(0)  # Yield control to allow other asyncio tasks to run
    return future.result()


class Drone:


    client = airsim.MultirotorClient()
    def __init__(self, x, y, z, DroneName = ""):
        #print("asd")
        self.client.enableApiControl(True, DroneName)
        #print("asd")
        self.client.armDisarm(True, DroneName)
        #print("asd")
        self.x = x
        self.y = y
        self.z = z
        self.client.takeoffAsync(vehicle_name=DroneName)
        #self.client.moveToPositionAsync(self.x, self.z, -self.y, 5).join()
        self.name = DroneName
        #,print("asd")
        #get gps data
        data = self.client.getGpsData(vehicle_name=DroneName)
        print("GPS data: %s" % data)


    def update(self):
        self.x = self.client.simGetGroundTruthKinematics(vehicle_name=self.name).position.x_val
        self.y = -1 * self.client.simGetGroundTruthKinematics(vehicle_name=self.name).position.z_val
        self.z = self.client.simGetGroundTruthKinematics(vehicle_name=self.name).position.y_val
        #print("Current location: (%f, %f, %f)" % (self.x, self.y, self.z))

    async def move(self, x, y, z, velocity, delay=0):
        #use sigmoid to calculate distance bound
        threshhold = 8 * (1 / (1 + np.exp(-1 * velocity)))  # 6 is the distance to target



        #adding rotation: we can either do it with absolute or relative degrees


        # Convert to float in case inputs are not in the correct format
        x, y, z = float(x), float(y), float(z)
        # Start moving to the position without waiting for it to complete
        await asyncio.sleep(delay)
        #print("a")
        self.client.moveToPositionAsync(x, z, -y, velocity, vehicle_name=self.name,drivetrain = 1, yaw_mode= airsim.YawMode(False,0))
        while True:
            await asyncio.sleep(0)
            self.update()
            location = np.array([self.x, self.y, self.z])
            target = np.array([x, y, z])
            distance = np.linalg.norm(location - target)
            #print("Distance to target: ", distance)
            #print("Current location: (%f, %f, %f)" % (self.x, self.y, self.z))
            if distance < threshhold:  # If within 6 meters of the target, cancel the task
                print("Drone %s has reached within %f meters of the target" % (self.name, threshhold))
                self.client.cancelLastTask(vehicle_name=self.name)
                break


        self.update()

    async def movegps(self, longitude, latitude, altitude, velocity, delay=0):
        #use sigmoid to calculate distance bound
        #print("ASKDHJASKLDJHASDJKL")
        #threshhold = 8 * (1 / (1 + np.exp(-1 * velocity)))  # 6 is the distance to target



        #adding rotation: we can either do it with absolute or relative degrees


        # Convert to float in case inputs are not in the correct format
        #x, y, z = float(x), float(y), float(z)
        # Start moving to the position without waiting for it to complete
        #await asyncio.sleep(delay)
        #print("a")
        self.client.moveToGPSAsync(latitude, longitude, altitude, velocity).join()
        '''while True:
            await asyncio.sleep(0)
            self.update()
            location = np.array([self.x, self.y, self.z])
            target = np.array([x, y, z])
            distance = np.linalg.norm(location - target)
            #print("Distance to target: ", distance)
            #print("Current location: (%f, %f, %f)" % (self.x, self.y, self.z))
            if distance < threshhold:  # If within 6 meters of the target, cancel the task
                print("Drone %s has reached within %f meters of the target" % (self.name, threshhold))
                self.client.cancelLastTask(vehicle_name=self.name)
                break'''


        #self.update()


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