import values
import numpy as np
import matplotlib.pyplot as plt
import copy
import scipy.integrate as integrate

# this class holds the state and information about the state variable


class State:

    def __init__(self, D=10, Ron=0.1, Roff=16, Mu=1e-10, intial=.76):
        self.D = D          # Semiconductor thickness
        self.Ron = Ron      # Maximum undoped
        self.Roff = Roff    # Maximum doped
        self.Mu = Mu        # Ion mobility

        self.currentState = intial

        self.time = np.arange(values.start, values.stop, values.steps)
        # These two arrays hold W and W/D as functions of time
        self.W = [0.0] * values.totalParts
        self.WD = [0.0] * values.totalParts
        self.W[0] = intial
        self.WD[0] = intial/self.D

    # callable gets W at a specific time
    def __call__(self, t):
        return self.W[values.getIndexFromT(t)] # if at zero don't subtract 1


    # calculates the rate of change of W(t) at any give point
    # pass in current to determine said rate
    def dwdt(self, current):
        return self.Mu * (self.Ron/self.D) * current

    # gets the instantaneous resistance of the device
    def instantResistance(self, t):
        return self.Ron * (self.__call__(t)/self.D) + (self.Roff * (1 -( self.__call__(t)/self.D))) # Equation 5 from the paper

    # gets the state of the device as a function of charge
    # equation 7
    def setWFromCharge(self, q, t):
        self.currentState = self.Mu * (self.Ron/self.D) * q(t) if t != 0.0 else self.currentState
        self.W[values.getIndexFromT(t)] = self.currentState
        self.WD[values.getIndexFromT(t)] = self.currentState / self.D

    # get W(t) from charge at a give point
    def setWAtTime(self, charge, t):
        pass

    # Returns WD array with index 0 being time
    def wd(self):
        return self.WD

    # returns the W array
    def w(self):
        return self.W
    def printState(self):
        print(self.currentState)

    def graphWD(self):
        plt.plot(self.time, self.WD)
        plt.show()

    # graph W
    def graphW(self):
        plt.plot(self.time, self.W)
        plt.show()


# This class deals with applied voltage
# set squared to two if you want the equation to be squared


class Voltage:

    def __init__(self, magnitude, frequency, squared=1):
        self.magnitude = magnitude        # amplitude of the sine wav
        self.omega = frequency * (2 * np.pi)

        self.time = np.arange(values.start, values.stop, values.steps)  # create the time

        self.amplitude = self.magnitude * (np.sin(self.omega * self.time) ** squared)

    # return the voltage at a given time
    def __call__(self, t):
        return self.current[values.getIndexFromT(t)]           # ----------------------- FIX THIS THIS IS WRONG


    # this graphs the sine wave
    def graph(self):
        plt.plot(self.time, self.amplitude)
        plt.xlabel('time')
        plt.ylabel('voltage')
        plt.grid(True, which='both')

        plt.show()

# This holds information for a current
class Current:

    CurrentAtPoint = [0.0] * values.totalParts       #This is for keeping track of the current at all points --Using a global is somewhat annoying attempt to fix later

    def __init__(self, voltage, state, t=0):

        self.voltage = voltage   # stores the voltage object
        self.state = state        #passed in state variable
        self.time = np.arange(values.start, values.stop, values.steps)

        self.current = self.setCurrent(t)   # set the current
        self.currentAtPoint = self.current[values.getIndexFromT(t)]   #set the current at that point


    def __call__(self, t):
        return self.current[values.getIndexFromT(t)]

    # get the current for resistance at an instantaneous point
    def setCurrent(self, t):

        toReturn = copy.deepcopy(self.voltage.amplitude)        #Copy the amps
        resistance = self.state.instantResistance(t)
        for index, volts in np.ndenumerate(self.voltage.amplitude):
            x = (volts / resistance)
            toReturn[index] = (volts / resistance)

        #set the current at a point
        self.CurrentAtPoint[values.getIndexFromT(t)] = (toReturn[values.getIndexFromT(t)])

        return toReturn


    def graphCurrentVsVoltage(self):

        plt.plot(self.time, self.CurrentAtPoint)
        plt.plot(self.time, self.voltage.amplitude)

        plt.show()

    def currentVoltage(self):
        y = [0.0]
        x = [0.0]
        for index, curr in enumerate(self.CurrentAtPoint):
            y.append(curr * 10000.0)
            x.append(self.voltage.amplitude[index])

        plt.scatter(x,y)
        plt.show()

class Charge:

    chargeAtAPoint = [0] * values.totalParts
    def __init__(self, current, state, voltage, t=0):

        self.current = current
        self.state = state
        self.voltage = voltage

        self.time = np.arange(values.start, values.stop, values.steps)

        self.charge = self.setCharge()                                      # set the charge
        self.chargeAtAPoint[values.getIndexFromT(t)] = self.charge[values.getIndexFromT(t)]       # set charge at a point

    def __call__(self, t):
        return self.charge[values.getIndexFromT(t)] # get the index at a point

    # get the charge
    def setCharge(self):
        return integrate.cumulative_trapezoid(self.current.current, self.time, initial=0)

    # graphs the charge
    def graph(self):
        plt.plot(self.time, self.charge)
        plt.show()

    # graph all three
    def graphVCI(self):
        fig, axs = plt.subplots(3)
        fig.suptitle('voltage -> current -> charge')
        axs[0].plot(self.time, self.voltage.amplitude)
        axs[1].plot(self.time, self.current.current)
        axs[2].plot(self.time, self.charge)

        plt.show()
'''
        plt.plot(self.time, self.current.current)
        plt.plot(self.time, self.voltage.amplitude)
        plt.plot(self.time, self.charge)

        plt.show()
'''