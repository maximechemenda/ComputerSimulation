import numpy as np

class Celestial(object):
    def __init__(self, dt, masses, positions, velocities): 
        #initialises the class
        self.G_CONSTANT = 6.67408e-11
        self.dt = dt
        self.ke = 0
        accelerations = np.zeros_like(positions)
        #accelerations = np.array([[ 5.30467516e-08,0.00000000e+00],[-3.94808531e-02,0.00000000e+00],[-1.13864515e-02,0.00000000e+00],[-5.93464473e-03,0.00000000e+00],[-2.55499347e-03,0.00000000e+00]]) 
        self.vectors = np.array([positions, velocities, accelerations])
        self.scalars = np.array([masses]) 
        self.calculate_acceleration() #sets a(-1) = a(0)
        self.orbital_period = 0
        self.potential_energies = np.zeros([len(self.vectors[2]), 1])
        self.potential_energy = 0
        self.total_energy = 0
        self.time = 0
        

    def calculate_next_acceleration(self):
        next_accelerations = np.zeros_like(self.vectors[0])

        for i in range(len(self.scalars[0])):    
            temp_accelerations = np.empty([len(self.vectors[2]), 2])
            temp_accelerations[i] = np.array([0, 0])
            for (j, m) in enumerate(self.scalars[0]):
                if j != i:
                    r1 = self.vectors[0][i] # position of the body with calculated acceleration
                    r2 = self.vectors[0][j] # position of the body that exerts a force on the body with calculated acceleration
                    temp_accelerations[j] = self.G_CONSTANT * m / ((np.linalg.norm(r2 - r1))**2) * (1 / (np.linalg.norm(r2 - r1))) * (r2 - r1)
            next_accelerations[i] = np.sum(temp_accelerations, axis=0)
        return next_accelerations

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

    def calculate_velocity(self, previous_accelerations, current_accelerations, next_accelerations):
        #calculates the velocity of all the bodies in the system 
        self.vectors[1] = self.vectors[1] + (1/6) * (2 * next_accelerations + 5 * current_accelerations - previous_accelerations) * self.dt

    def calculate_position(self, previous_accelerations, current_accelerations):
        #calculates and updates the positions of all the bodies in the system 
        self.vectors[0] = self.vectors[0] + self.vectors[1] * self.dt + (1/6) * (4 * current_accelerations - previous_accelerations) * self.dt * self.dt

    def calculate_ke(self):
        temp_ke = np.zeros(len(self.vectors[2]))
        for i in range(len(self.vectors[2])):
            temp_ke[i] = 1/2 * self.scalars[0][i] * np.linalg.norm(self.vectors[1][i])**2
        self.ke = np.sum(temp_ke)


    def is_orbital_period(self, previous_positions):
        if previous_positions[3][1] < 0 and self.vectors[0][3][1] >= 0:
            return True
        return False

    def seconds_to_years(self, sec):
        minutes = sec / 60
        hours = minutes / 60
        days = hours / 24
        years = days / 365.25
        return years

    def calculate_potential_energy(self):
        for i in range(len(self.scalars[0])):    
            temp_energies = np.empty([len(self.vectors[2]), 1])
            temp_energies[i] = 0
            for (j, m) in enumerate(self.scalars[0]):
                if j != i:
                    r1 = self.vectors[0][i] # position of the body with calculated acceleration
                    r2 = self.vectors[0][j] # position of the body that exerts a force on the body with calculated acceleration
                    m1 = self.scalars[0][i]
                    m2 = self.scalars[0][j]
                    temp_energies[j] = (-1/2) * ((self.G_CONSTANT * m1 * m2) / (np.linalg.norm(r2 - r1)))
            self.potential_energies[i] = np.sum(temp_energies, axis=0)
            self.potential_energy = np.sum(self.potential_energies)

    def calculate_total_energy(self):
        self.total_energy = self.ke + self.potential_energy

        # Write the energy to the file.
        text = ("Energy: " + str(self.total_energy) + " J.\n")
        with open("energies.txt", "a") as energies_file:
            energies_file.write(text)

    












"""
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
        #calculates the acceleration of all the bodies in the system 
        #uses the formula with the sum of the gravitational forces exerted by all the other bodies in the system
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
"""