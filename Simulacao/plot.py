import matplotlib.pyplot as plt
import os

def plot_fitness(fit, fitavg):
    plt.plot(fit, label = 'fit_best', color='tab:red')
    plt.plot(fitavg, label = 'fit_avg', color='tab:orange')

    plt.title('Fitness do melhor individuo e da média para cada geração')
    plt.tight_layout()
    plt.legend()
    plt.show()

def plot_params_from_log():
    individuos = []
    logs = os.listdir('logs/')
    if(len(logs) > 0):
        logs.sort()
        for log in logs:
            log = open("logs/" + str(log), "r")
            for linha in log:
                data = linha.rstrip()
                data = data.split(',')
                individuos.append((float(data[0]), float(data[1]), float(data[2])))
                break

        plt.plot(individuos)
        plt.show()
