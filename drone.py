#drone class for airsim
import airsim
import time
import asyncio

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
