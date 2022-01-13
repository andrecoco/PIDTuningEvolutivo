import matplotlib.pyplot as plt
import numpy as np

def plot_graph(temps, pot, N_MEDIDAS, Kp, Ki, Kd, set_point):
    # Data for plotting
    t = np.linspace(0, N_MEDIDAS//2, N_MEDIDAS)

    plt.plot(t, temps, label = 'temp', color='tab:red')
    plt.title('Kp = {}, Ki = {}, Kd = {}, Setpoint = {}'.format(Kp, Ki, Kd, set_point))

    plt.plot(t, pot, label = 'pot', color='tab:blue')

    plt.tight_layout()
    plt.legend()
    plt.show()

def plot_fitness(fit, fitavg):
    plt.plot(fit, label = 'fit_best', color='tab:red')
    plt.plot(fitavg, label = 'fit_avg', color='tab:orange')

    plt.title('Fitness do melhor individuo e da média para cada geração')
    plt.tight_layout()
    plt.legend()
    plt.show()
