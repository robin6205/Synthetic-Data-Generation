#drone class for airsim
import airsim
import time

class Drone:
    def __init__(self, client, x, y, z):
        self.client = client
        self.x = x
        self.y = y
        self.z = z
        self.client.takeoffAsync().join()
        self.client.moveToPositionAsync(self.x, self.z, -self.y, 5).join()

    def update(self):
        self.x = self.client.simGetGroundTruthKinematics().position.x_val
        self.y = self.client.simGetGroundTruthKinematics().position.y_val
        self.z = self.client.simGetGroundTruthKinematics().position.z_val
        print("Current location: (%f, %f, %f)" % (self.x, self.z, -self.y))
    def move(self, x, y, z,velocity):
        try:
            x = float(x)
            y = float(y)
            z = float(z)
            velocity = float(velocity)
        except ValueError:
            print("Invalid input. Please enter a number.")
            return

        x = float(x)
        y = float(y)
        z = float(z)

        self.client.moveToPositionAsync(x, z, -y, velocity).join()
        self.update()
    def orbit(self,x,y,z,radius,orbits):
        try:
            x = float(x)
            y = float(y)
            z = float(z)
            radius = float(radius)
            orbits = int(orbits)
        except ValueError:
            print("Invalid input. Please enter a number.")
            return

        for i in range(orbits):
            self.client.moveToPositionAsync(x+radius, z, -y, 5).join()
            self.client.moveToPositionAsync(x, z+radius, -y, 5).join()
            self.client.moveToPositionAsync(x-radius, z, -y, 5).join()
            self.client.moveToPositionAsync(x, z-radius, -y, 5).join()
        self.update()
