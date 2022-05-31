import ohm
import values
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    # create these first
    volts = ohm.Voltage(1, 5)
    state = ohm.State()
    one, axs = plt.subplots(3)

    for index, x in enumerate(volts.amplitude):
        time = values.getTimeFromIndex(index)               # get the time

        current = ohm.Current(volts, state, time)           # update current
        charge = ohm.Charge(current, state, volts, time)    # update charge
        state.setWFromCharge(charge, time)                  # set the charge'
        #for testing -----------------------------------------------------
        one, axs = plt.subplots(3)
        if index%100 == 0:
            one.suptitle('voltage -> current -> charge')
            axs[0].plot(np.arange(values.start, values.stop, values.steps), volts.amplitude)
            axs[1].plot(np.arange(values.start, values.stop, values.steps), current.current)
            axs[2].plot(np.arange(values.start, values.stop, values.steps), charge.charge)
        # for testing ----------------------------------------------------------------------------
    plt.plot()
    state.graphWD()


 #   volts.graph()
 #   current.graphCurrentVsVoltage()
 #   charge.graph()

 #   charge.graphVCI()

