class Polynomial(object):
    def __init__(self, coefficients):
        # initialises the instance variable coefficients
        self.coefficients = coefficients

        while self.coefficients[-1] == 0:
            self.coefficients = self.coefficients[:-1]

    def order(self):
        # returns the order of the polynomial, which is the length of the coefficient list substracted by 1
        return len(self.coefficients) - 1 

    def __add__(self,p2):
        """
        calculates the sum of two polynomials using list comprehension. There is a comparison between the 
        length of the lists of coefficients as there are three different cases to consider: 
            - the two polynomials have the same order
            - the order of the first polynomial is higher than the order of the second one
            - the order of the second polynomial is higher than the order of the first one
        """
        len1 = len(self.coefficients)
        len2 = len(p2.coefficients)
        if len1 == len2:
            sum_polynomial = list([x + y for x, y in zip(self.coefficients, p2.coefficients)])
        elif len1 > len2:
            sum_polynomial = list([x + y for x, y in zip(self.coefficients, p2.coefficients)]) + self.coefficients[len2:]
        else:
            sum_polynomial = list([x + y for x, y in zip(self.coefficients, p2.coefficients)]) + p2.coefficients[len1:]
        return Polynomial(sum_polynomial)

    def derivative(self):
        """
        returns the derivative of the polynomial
        """
        return Polynomial([self.coefficients[k]*k for k in range(1,len(self.coefficients))])

    def antiderivative(self,c):
        """
        returns the antiderivative of the polynomial
        """
        return Polynomial([c] + [self.coefficients[k]*(1/(k+1)) for k in range(0,len(self.coefficients))])

    def __str__(self):
        """
        prints a sensible String representation of the polynomial in the form 
        P(x) = a0 + a1x + a2x^2 + ... + anx^n
        """
        if not self.coefficients:
            return "P(x) = 0"
        string_polynomial = ""
        for power in range(len(self.coefficients)):
            if self.coefficients[power] == 0:
                pass
            elif power == 0:
                if self.coefficients[power] < 0:
                    string_polynomial += " - " + str(self.coefficients[power] * (-1))
                else:
                    string_polynomial += " + " + str(self.coefficients[power]) 
            elif power == 1:
                if self.coefficients[power] < 0:
                    string_polynomial += " - " + str(self.coefficients[power] * (-1)) + "x"
                else:
                    string_polynomial +=" + " + str(self.coefficients[power]) + "x"    
            elif self.coefficients[power] < 0:
                string_polynomial += " - " + str(self.coefficients[power] * (-1)) + "x^" + str(power)
            else:
                string_polynomial += " + " + str(self.coefficients[power]) + "x^" + str(power) 

            if string_polynomial[:3] == " + ":
                string_polynomial = string_polynomial[3:]
        return string_polynomial