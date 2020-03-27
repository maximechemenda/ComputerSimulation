from juliaset import Julia 

class JuliaTest(object):

    def run(self):
        xmin = -2.025
        xmax = 2.025
        ymin = -1.125
        ymax = 1.125
        width = 500
        height = 500
        maxiter = 255
        number = complex(0.3, 0.6)
        jul = Julia(xmin, xmax, ymin, ymax, width, height, maxiter, number) 
        jul.plot_mandelbrot()

if __name__ == "__main__":
    test = JuliaTest()
    test.run()