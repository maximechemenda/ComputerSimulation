import numpy as np

class Celestial(object):
    def __init__(self, dt, masses, positions, velocities): 
        #initialises the class
        self.G_CONSTANT = 6.67408e-11
        self.dt = dt
        self.ke = []
        accelerations = np.zeros_like(positions)
        self.vectors = np.array([positions, velocities, accelerations])
        self.scalars = np.array([masses]) 
    
    def calculate_acceleration(self):
        """
        calculates the acceleration of all the bodies in the system 
        uses the formula with the sum of the gravitational forces exerted by all the other bodies in the system
        """
        for i in range(len(self.scalars[0])):    
            temp_accelerations = np.empty([len(self.vectors[2]), 2])
            temp_accelerations[i] = np.array([0, 0])
            for (j, m) in enumerate(self.scalars[0]):
                if j != i:
                    r1 = self.vectors[0][i] # position of the body with calculated acceleration
                    r2 = self.vectors[0][j] # position of the body that exerts a force on the body with calculated acceleration
                    temp_accelerations[j] = self.G_CONSTANT * m / ((np.linalg.norm(r2 - r1))**2) * (1 / (np.linalg.norm(r2 - r1))) * (r2 - r1)
            self.vectors[2][i] = np.sum(temp_accelerations, axis=0) 

    def calculate_velocity(self):
        #calculates the velocity of all the bodies in the system 
        self.vectors[1] = self.vectors[1] + (self.dt * self.vectors[2])

    def calculate_position(self):
        #calculates and updates the positions of all the bodies in the system 
        self.vectors[0] = self.vectors[0] + (self.dt * self.vectors[1])

    def calculate_ke(self):
        #calculates the total kinetic energy (ke) of the system 
        ke = 0.5 * self.scalars[0] * (np.linalg.norm(self.vectors[1], axis=1))**2
        self.ke.append(np.sum(ke))