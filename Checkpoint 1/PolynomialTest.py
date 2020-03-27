from Polynomial import Polynomial

class PolynomialTest(object):

    def run(self):

        poly1 = Polynomial([2,0,4,-1,0,6]) 
        
        poly2 = Polynomial([-1,-3,0,4.5]) 

        print("The order of the polynomial (P1(x) = " + str(poly1) + ") is " + str(poly1.order()))

        print("The sum of the polynomials (P1(x) = " + str(poly1) + ") and (P2(x) = " + str(poly2) + ") is " + str(poly1 + poly2))

        print("The derivative of the polynomial (P1(x) = " + str(poly1) + ") is " + str((poly1.derivative())))

        print("The antiderivative of the derivative of (P(x) = " + str(poly1) + ") is " + str((poly1.derivative()).antiderivative(2)))

if __name__ == "__main__":
    test = PolynomialTest()
    test.run()