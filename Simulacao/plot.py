from cProfile import label
import matplotlib.pyplot as plt
import os

# realiza o plot da evolucao do fitness do melhor individuo e a media da populacao
def plot_fitness(fit, fitavg):
    plt.plot(fit, label = 'fit_best', color='tab:red')
    plt.plot(fitavg, label = 'fit_avg', color='tab:orange')

    plt.title('Fitness do melhor individuo e da média para cada geração')
    plt.tight_layout()
    plt.legend()
    plt.show()

# realiza o plot da evolucao dos genes a partir dos logs salvos
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
        
        labels = ["KP", "KI", "KD"]
        plt.plot(individuos)
        plt.legend(labels)
        plt.title("Variação dos valores de KP, KI e KD")
        plt.tight_layout()
        plt.show()
