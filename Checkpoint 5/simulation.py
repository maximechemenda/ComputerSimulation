import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
from Celestial import Celestial

G_CONSTANT = 6.67408e-11

class Simulation:
    def __init__(self):
        """
        initialises the class
        gets parameters from the given file
        creates arrays containing the masses, positions and velocities of all the bodies in the system
        """
        parameters = np.genfromtxt("test_data4.txt", delimiter=',', skip_header=1, usecols=(1, 2, 3, 4, 5)) 
        mass = [] 
        position = [] 
        velocity = [] 

        for body in range(parameters[:, 0].size):
            mass.append(np.array([parameters[body][0]]))
            position.append(np.array([parameters[body][1], parameters[body][2]]))
            velocity.append(np.array([parameters[body][3], parameters[body][4]]))

        masses = np.array(mass)
        positions = np.array(position)
        velocities = np.array(velocity)
        
        #calculates initial velocities for the moons 
        for i in range(1, parameters[:, 0].size):
            velocities[i][1] = (G_CONSTANT * masses[0] / (np.linalg.norm(positions[i] - positions[0]))) ** 0.5
        
        self.system = Celestial(500, masses, positions, velocities)

        #sets up simulation parameters
        self.colours = ['red', 'gray', 'yellow', 'blue']
        self.niter = 30000

    def init(self):
        #initialiser for animator
        return self.patches

    def animate(self, i): 
        """
        updates the positions of the bodies of the system 
        prints the total kinetic energy at regular intervals
        """
        self.system.calculate_acceleration()
        self.system.calculate_velocity()
        self.system.calculate_position()

        #prints the total kinetic energy
        if i % 250 == 0:
            self.system.calculate_ke()
            print("ke: " + str(self.system.ke))

        #updates the positions of the bodies 
        for x in range(0, len(self.patches)):
            self.patches[x].center = self.system.vectors[0][x]
            
        return self.patches

    def run(self):
        #creates plot elements
        fig = plt.figure()
        ax = plt.axes() 

        #creates list for the bodies
        self.patches = []

        #creates circles corresponding to the bodies
    
        for i in range(0, self.system.scalars[0].size):
            self.patches.append(plt.Circle((self.system.vectors[0][i]), 1.5e5, color=self.colours[i], animated=True))
        #adds circles to axes
        for i in range(0, len(self.patches)):
            ax.add_patch(self.patches[i])

        #set up the axes
        ax.axis('scaled')
        ax.set_xlim(-25e06, 25e06) #values chosen according to the orbital radius r13
        ax.set_ylim(-25e06, 25e06) #values chosen according to the orbital radius r13
        ax.patch.set_facecolor('black')

        #creates the animator
        anim = FuncAnimation(fig, self.animate, init_func=self.init, frames=self.niter, repeat=False, interval=30, blit=True)

        #shows the plot
        plt.show()

    