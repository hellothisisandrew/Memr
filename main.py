import ohm
import values
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    # create these first
    volts = ohm.Voltage(1, 5)
    state = ohm.State(intial=.96)

    for index, x in enumerate(volts.amplitude):
        time = values.getTimeFromIndex(index)             # get the time

        current = ohm.Current(volts, state, time)
       # current.graphCurrentVsVoltage()
        charge = ohm.Charge(current, state, volts, time)    # update charge
        state.setWFromCharge(charge, time)
        state.printState()# set the charge'
        #for testing -----------------------------------------------------
        # for testing ----------------------------------------------------------------------------

    current = ohm.Current(volts, state, .01)
    current.currentVoltage()

    state.graphWD()
    state.graphW()




 #   volts.graph()
 #   current.graphCurrentVsVoltage()
 #   charge.graph()

 #   charge.graphVCI()

