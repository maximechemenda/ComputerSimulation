import numpy as np
import matplotlib.pyplot as plt

class Julia(object):
  
    def __init__(self, xmin, xmax, ymin, ymax, width, height, maxiter, number):
        """
        initialises the class with all the data needed to plot the mandelbrot set 
        width and height set the dimension of the image
        maxiter is the number of iterations such that if a complex number hasn't diverged after this number, then it is within the mandelbrot set
        """ 
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.width = width
        self.height = height
        self.maxiter = maxiter
        self.number = number
        self.mandelbrot_atlas = np.empty((self.width, self.height))

    def mandelbrot_function(self, complex_number):
        # calculates the number of iterations it takes for a complex number to diverge 
        for num_iterations in range(self.maxiter):
            if abs(complex_number) > 2:
                return num_iterations
            complex_number = complex_number * complex_number + self.number
        return 0 

    def mandelbrot_points(self):
        # assigns points to the mandelbrot atlas for plotting by calling the mandelbrot function
        real = np.linspace(self.xmin, self.xmax, self.width)
        imaginary = np.linspace(self.ymin, self.ymax, self.height)

        for i in range(self.width):
            for j in range(self.height):
                self.mandelbrot_atlas[j,i] = self.mandelbrot_function(complex(real[i], imaginary[j]))

    def plot_mandelbrot(self):
        """
        plots the mandelbrot set with matplotlib
        calls the mandelbrot_points method to give values to the atlas
        """
        self.mandelbrot_points()
        plt.imshow(self.mandelbrot_atlas, cmap = "hot", extent=[self.xmin, self.xmax, self.ymin, self.ymax])
        plt.ylabel("Imaginary Axis")
        plt.xlabel("Real Axis")
        plt.title("Julia Set")
        plt.show()