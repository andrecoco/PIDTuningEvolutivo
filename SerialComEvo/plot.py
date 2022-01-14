import matplotlib.pyplot as plt
import numpy as np

# realiza o plot da potencia e temperatura pelo tempo
def plot_graph(temps, pot, N_MEDIDAS, Kp, Ki, Kd, set_point):
    # Data for plotting
    t = np.linspace(0, N_MEDIDAS//2, N_MEDIDAS)

    color = 'tab:red'
    fig, ax1 = plt.subplots()
    ax1.plot(t, temps, label = 'temp', color=color)
    ax1.set_ylabel('temp', color=color)
    ax1.set(xlabel='tempo (s)',
        title='Kp = {}, Ki = {}, Kd = {}, Setpoint = {}'.format(Kp, Ki, Kd, set_point))
    ax1.grid()

    color = 'tab:blue'  
    ax2 = ax1.twinx()
    ax2.plot(t, pot, label = 'pot', color=color)
    ax2.set_ylabel('pot', color=color)

    plt.tight_layout()
    plt.legend()
    plt.show()

# realiza o plot da evolucao do fitness do melhor individuo e a media da populacao
def plot_fitness(fit, fitavg):
    plt.plot(fit, label = 'fit_best', color='tab:red')
    plt.plot(fitavg, label = 'fit_avg', color='tab:orange')

    plt.title('Fitness do melhor individuo e da média para cada geração')
    plt.tight_layout()
    plt.legend()
    plt.show()