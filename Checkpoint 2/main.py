from Decay import Decay

class Main(object):

    def run(self):
        
        input_constant = float(input("Decay constant: "))
        input_length = int(input("Length: "))
        input_timestep = float(input("Timestep: "))

        iode = Decay(input_constant, input_length, input_timestep)

        iode.sim_halflife()

        print(str(iode))

        print("The initial number of undecayed nuclei is: " + str(iode.initial_undecayed()))

        print("The final number of undecayed nuclei is: " + str(iode.final_undecayed()))

        print("The simulated half-life is: " + str(iode.sim_halflife()) + " minutes.")

        print("The actual half-life is: " + str(iode.actual_halflife()) + " minutes.")


if __name__ == "__main__":
    test = Main()
    test.run()