import matplotlib.pyplot as plt
import numpy as np

def plot_graph(temps, pot, N_MEDIDAS, Kp, Ki, Kd, set_point):
    # Data for plotting
    t = np.linspace(0, N_MEDIDAS//2, N_MEDIDAS)

    color = 'tab:red'
    fig, ax1 = plt.subplots()
    ax1.plot(t, temps, label = 'temp', color=color)
    ax1.set_ylabel('temp', color=color)
    ax1.set(xlabel='tempo (s)',
        title='Kp = {}, Ki = {}, Kd = {}, Setpoint = {}'.format(Kp, Ki, Kd, set_point))
    #ax1.set_ylim([50, 1.1*float(set_point)])
    ax1.grid()

    color = 'tab:blue'  
    ax2 = ax1.twinx()
    ax2.plot(t, pot, label = 'pot', color=color)
    ax2.set_ylabel('pot', color=color)
    #ax2.set_ylim([0, 1.1*256])

    plt.tight_layout()
    plt.legend()
    plt.show()