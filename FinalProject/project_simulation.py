import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
from project_celestial import Celestial

G_CONSTANT = 6.67408e-11

class Simulation:
    def __init__(self):
        """
        initialises the class
        gets parameters from the given file
        creates arrays containing the masses, positions and velocities of all the bodies in the system
        """
        parameters = np.genfromtxt("project_data.txt", delimiter=',', skip_header=1, usecols=(1, 2, 3, 4, 5)) 
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
        
        self.system = Celestial(500000, masses, positions, velocities)
        
        #sets up simulation parameters
        self.colours = ['yellow', 'gray', 'white', 'blue','red']
        self.size = [1.64e10, 5.7e8, 1.4e9, 1.5e9, 7.98e8]
        #self.size = [1.64e11, 5.7e8, 1.4e9, 1.5e9, 7.98e8]
        self.niter = 30000

        self.energies = []
        self.times = []


    def init(self):
        #initialiser for animator
        return self.patches

    def animate(self, i): 
        """
        updates the positions of the bodies of the system 
        prints the total kinetic energy at regular intervals
        """

        #updates the accelerations, velocities and positions using the Beeman algorithm
        previous_positions = np.copy(self.system.vectors[0])
        previous_accelerations = np.copy(self.system.vectors[2])
        self.system.calculate_acceleration()
        current_accelerations = np.copy(self.system.vectors[2])
        self.system.calculate_position(previous_accelerations, current_accelerations)   
        next_accelerations = self.system.calculate_next_acceleration()
        self.system.calculate_velocity(previous_accelerations, current_accelerations, next_accelerations)

        #prints the period of the Earth
        if self.system.is_orbital_period(previous_positions):
            print("Period of the Earth: " + str(self.system.seconds_to_years(self.system.orbital_period)) + " Earth years.")
            self.system.orbital_period = 0
        self.system.orbital_period += self.system.dt

        #updates the time
        self.system.time += self.system.dt

        #calculates total energy
        self.system.calculate_ke()
        self.system.calculate_potential_energy()
        self.system.calculate_total_energy()

        self.energies.append(self.system.total_energy) # appends the new total energy to the list containing all the previous total energies
        self.times.append(self.system.time) # appends the new time to the list containing all the previous times

    

        #prints the total energy
        if i % 250 == 0:
            print("total energy: " + str(self.system.total_energy))
            
        #updates the positions of the bodies 
        for x in range(0, len(self.patches)):
            self.patches[x].center = self.system.vectors[0][x]

        return self.patches

    """
    def plot_energy(self):
        plt.plot(self.times, self.energies)
        plt.xlabel('Time (s)')
        plt.ylabel('Energy (J)')
        plt.show()
    """

    def run(self):
        #creates plot elements
        fig = plt.figure()
        ax = plt.axes() 

        #creates list for the bodies
        self.patches = []

        #creates circles corresponding to the bodies
    
        for i in range(0, self.system.scalars[0].size):
            self.patches.append(plt.Circle((self.system.vectors[0][i]), self.size[i], color=self.colours[i], animated=True))
        #adds circles to axes
        for i in range(0, len(self.patches)):
            ax.add_patch(self.patches[i])

        #set up the axes
        ax.axis('scaled')
        ax.set_xlim(-235e09, 235e09) #values chosen according to the orbital radius r13
        ax.set_ylim(-235e09, 235e09) #values chosen according to the orbital radius r13
        ax.patch.set_facecolor('black')

        #creates the animator
        anim = FuncAnimation(fig, self.animate, init_func=self.init, frames=self.niter, repeat=False, interval=50, blit=True)

        #shows the plot
        plt.show()

        

        
        
    


"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
from project_celestial import Celestial

G_CONSTANT = 6.67408e-11

class Simulation:
    def __init__(self):
        #initialises the class
        #gets parameters from the given file
        #creates arrays containing the masses, positions and velocities of all the bodies in the system
        parameters = np.genfromtxt("project_data.txt", delimiter=',', skip_header=1, usecols=(1, 2, 3, 4, 5)) 
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
        
        self.system = Celestial(500000, masses, positions, velocities)

        #sets up simulation parameters
        self.colours = ['yellow', 'gray', 'white', 'blue','red']
        self.size = [1.64e10, 5.7e8, 1.4e9, 1.5e9, 7.98e8]
        #self.size = [1.64e11, 5.7e8, 1.4e9, 1.5e9, 7.98e8]
        self.niter = 30000

    def init(self):
        #initialiser for animator
        return self.patches

    def animate(self, i): 
        #updates the positions of the bodies of the system 
        #prints the total kinetic energy at regular intervals
        self.system.calculate_acceleration()
        self.system.calculate_velocity()
        self.system.calculate_position()

        #prints the total kinetic energy
        if i % 250 == 0:
            self.system.calculate_ke()
            print(self.system.ke)

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
            self.patches.append(plt.Circle((self.system.vectors[0][i]), self.size[i], color=self.colours[i], animated=True))
        #adds circles to axes
        for i in range(0, len(self.patches)):
            ax.add_patch(self.patches[i])

        #set up the axes
        ax.axis('scaled')
        ax.set_xlim(-235e09, 235e09) #values chosen according to the orbital radius r13
        ax.set_ylim(-235e09, 235e09) #values chosen according to the orbital radius r13
        ax.patch.set_facecolor('black')

        #creates the animator
        anim = FuncAnimation(fig, self.animate, init_func=self.init, frames=self.niter, repeat=False, interval=50, blit=True)

        #shows the plot
        plt.show()
"""
    