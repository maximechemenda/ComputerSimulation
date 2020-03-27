from random import random
import numpy as np
from math import log

class Decay(object):

    def __init__(self, constant, length, timestep):
        # initialises the different instance varibales 
        self.constant = constant
        self.length = length 
        self.timestep = timestep 
        self.halflife = 0
        self.initial_nuclei = length * length
        self.undecayed_nuclei = length * length
        self.probability = constant * timestep 
        self.matrix = [[ 1 for _ in range(length) ] for _ in range(length) ]

    def sim_halflife(self):
        """
        simulates the half-life of the Iodine-128
        if the random probability is smaller than the given probability then the nuclius is decayed so the number of undecayed nuclei decreases by 1
        terminates when the number of undecayed nuclei has fallen to half of the value initial value
        """
        while self.undecayed_nuclei > self.initial_nuclei / 2: 
            for i in range(self.length):
                for j in range(self.length): 
                    if self.matrix[i][j] == 1 and random() <= self.probability:
                        self.matrix[i][j] = 0 
                        self.undecayed_nuclei -= 1
            self.halflife += self.timestep
        return self.halflife

    def __str__(self):
        """
        prints a visual representation of the array of nuclei
        the number 1 represents an undecayed nuclius
        the number 0 represents a decayed nuclius
        """
        pretty_matrix = ""
        for i in range(self.length):
            for j in range(self.length):
                if j == self.length - 1:
                    pretty_matrix += " " + str(self.matrix[i][j]) + "\n"
                else:
                    pretty_matrix += " " + str(self.matrix[i][j])
        return pretty_matrix

    def initial_undecayed(self):
        #returns the initial number of undecayed nuclei
        return self.initial_nuclei 

    def final_undecayed(self):
        #returns the final number of undecayed nuclei
        return self.undecayed_nuclei 

    def actual_halflife(self):
        #returns the actual value of the half=lifem as given by the decat constant
        return log(2) / self.constant