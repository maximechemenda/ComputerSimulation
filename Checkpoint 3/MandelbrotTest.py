from mandelbrot import Mandelbrot 

class MandelbrotTest(object):

    def run(self):
        xmin = -2.025
        xmax = 0.6
        ymin = -1.125
        ymax = 1.125
        width = 400
        height = 400
        maxiter = 255
        mandel = Mandelbrot(xmin, xmax, ymin, ymax, width, height, maxiter) 
        mandel.plot_mandelbrot()

if __name__ == "__main__":
    test = MandelbrotTest()
    test.run()