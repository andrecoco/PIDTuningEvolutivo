from random import uniform, choices
import controle
import os
import numpy as np
import plot

# DEFINES
## POPULACAO
NUMERO_DE_INDIVIDUOS_POR_THREAD = 5
MUTACAO = None #%
TAXAS_MUTACAO = [0.25, 1] #%
#TAXAS_MUTACAO = 6*[0.25] #caso queira mutação fixa
LIMITE_CONTADOR = 10 #depois de quantas geracoes sem melhoria alterar a taxa de mut
N_CICLOS_MUT = 4
CHANCE_MUT = 1
TEM_GENOCIDIO = True
DELTA = 0.01
TEM_PREDACAO_RANDOMICA = True
N_GERACOES_PREDACAO = 5 #numero de geracoes entre predacoes
N_PREDADOS = 1 #numero de piores individuos que vao ser predados

## INDIVIDUO
MAX_KP = 20
MIN_KP = 0.1
RANGE_KP = MAX_KP
MAX_KI = 20
MIN_KI = 0.1
RANGE_KI = MAX_KI
MAX_KD = 0
MIN_KD = 0
RANGE_KD = MAX_KD
PRECISAO = 3  #CASAS DECIMAIS DE PRECISAO

## TESTE
N_MEDIDAS = 200 #Arduino
N_SEGUNDOS = 100 #Simulacao
RECUPERA_LOG = True

## MULTITHREADING
NUMERO_DE_THREADS = 1

class Individuo:
    def __init__(self, *args) -> None:
        if (len(args) == 4):
            self.fitness = float(args[3])
            self.Kp = float(args[0])
            self.Ki = float(args[1])
            self.Kd = float(args[2])
        else:
            self.fitness = None
            self.Kp = round(uniform(MIN_KP, MAX_KP), PRECISAO)
            self.Ki = round(uniform(MIN_KI, MAX_KI), PRECISAO)
            self.Kd = round(uniform(MIN_KD, MAX_KD), PRECISAO)

    def __lt__(self, other) -> None:
        return self.fitness < other.fitness

    def __str__(self) -> str:
        return "{},{},{},{}".format(self.Kp, self.Ki, self.Kd, self.fitness)

    def cruzamento(self, parceiro):
        self.Kp = round((parceiro.Kp + self.Kp)/2 + choices([1, 0], [CHANCE_MUT, 1-CHANCE_MUT])[0]*uniform(-1*(MUTACAO/100)*RANGE_KP, (MUTACAO/100)*RANGE_KP), PRECISAO)
        self.Ki = round((parceiro.Ki + self.Ki)/2 + choices([1, 0], [CHANCE_MUT, 1-CHANCE_MUT])[0]*uniform(-1*(MUTACAO/100)*RANGE_KI, (MUTACAO/100)*RANGE_KI), PRECISAO)
        self.Kd = round((parceiro.Kd + self.Kd)/2 + choices([1, 0], [CHANCE_MUT, 1-CHANCE_MUT])[0]*uniform(-1*(MUTACAO/100)*RANGE_KD, (MUTACAO/100)*RANGE_KD), PRECISAO)
        self.fitness = None

        if(self.Kp < MIN_KP):
            self.Kp = MIN_KP
        elif(self.Kp > MAX_KP):
            self.Kp = MAX_KP

        if(self.Ki < MIN_KI):
            self.Ki = MIN_KI
        elif(self.Ki > MAX_KI):
            self.Ki = MAX_KI
        
        if(self.Kd < MIN_KD):
            self.Kd = MIN_KD
        elif(self.Kd > MAX_KD):
            self.Kd = MAX_KD
        
    def reset_genes(self):
        self.fitness = None
        self.Kp = round(uniform(MIN_KP, MAX_KP), PRECISAO)
        self.Ki = round(uniform(MIN_KI, MAX_KI), PRECISAO)
        self.Kd = round(uniform(MIN_KD, MAX_KD), PRECISAO)


def test_fitness(individuo):
    return (individuo.Kp + individuo.Ki + individuo.Kd)

def print_bonito(array):
    for item in array:
        print(item)
    print()

def escreve_log(geracao, individuos):
    f = open("logs/" + str(geracao) + ".txt", "w")
    for individuo in individuos:
        f.write(str(individuo) + "\n")
    f.close()

def recupera_log():
    logs = os.listdir('logs/')
    if(len(logs) > 0 and RECUPERA_LOG):
        logs.sort()
        log = open("logs/" + str(logs[-1]), "r")
        geracao = int(logs[-1][:-4])
        individuos = []
        for linha in log:
            data = linha.rstrip()
            data = data.split(',')
            individuos.append(Individuo(data[0], data[1], data[2], data[3]))
        return individuos, geracao + 1
    return None, None

def inicializa_populacao():
    #Verifica se existem logs para continuar de onde parou
    individuos, geracao = recupera_log()

    #Começa do zero
    if (individuos is None):
        individuos = []
        geracao = 0
        for i in range(NUMERO_DE_INDIVIDUOS_POR_THREAD*NUMERO_DE_THREADS):
            novo_indiv = Individuo()
            individuos.append(novo_indiv)
    return individuos, geracao

def espalha_genes_elitismo(individuos, geracao):
    if(TEM_PREDACAO_RANDOMICA and geracao%N_GERACOES_PREDACAO == 0):
        antes = individuos[0]
        for individuo in individuos[1:-1*N_PREDADOS]:
            individuo.cruzamento(individuos[0])
        depois = individuos[0]
        if(antes != depois):
            print("AAAAAAAAAAAAAAAAAAAAAAAA")
        
        #predacao randomica
        for individuo in individuos[-1*N_PREDADOS:]:
            individuo.reset_genes()
    else:
        antes = individuos[0]
        for individuo in individuos[1:]:
            individuo.cruzamento(individuos[0])
        depois = individuos[0]
        if(antes != depois):
            print("AAAAAAAAAAAAAAAAAAAAAAAA")

def genocidio(individuos):
    for individuo in individuos[1:]:
        individuo.reset_genes()

if __name__ == "__main__":
    individuos, geracao = inicializa_populacao()

    # Mutacao variavel
    contador = 0 #pra mutacao variavel
    ciclos_mutacao = 0
    old_best = np.inf
    index_mut = 0
    MUTACAO = TAXAS_MUTACAO[index_mut]

    plot_fit = []
    plot_avgfit = []

    while(True):
        print(geracao)

        if(geracao == 0):
            for individuo in individuos:
                individuo.fitness = controle.test_tuning(individuo.Kp, individuo.Ki, individuo.Kd, N_MEDIDAS)   

        else:
            for individuo in individuos[1:]:
                individuo.fitness = controle.test_tuning(individuo.Kp, individuo.Ki, individuo.Kd, N_MEDIDAS)

        individuos.sort() #coloca o melhor na frente, para nao mata-lo

        #PARA O PLOT
        plot_fit.append(1/(individuos[0].fitness))
        plot_avgfit.append(1/(np.average([ind.fitness for ind in individuos])))

        #LOGS
        if(geracao%10 == 0):
            escreve_log(geracao, individuos)

        # MUTACAO DINAMICA
        #ve se melhorou nas ultimas 2 geracoes
        if(abs(individuos[0].fitness - old_best) <= DELTA):
            contador += 1
        else: #se melhorou
            print("melhorou na geracao {} :) - mut = {}%".format(geracao, MUTACAO))
            contador = 0
            index_mut = 0
            MUTACAO = TAXAS_MUTACAO[index_mut]
            ciclos_mutacao = 0
        
        if(contador >= LIMITE_CONTADOR):
            contador = 0
            index_mut += 1
            if(index_mut >= len(TAXAS_MUTACAO)):
                if(TEM_GENOCIDIO):
                    genocidio(individuos)
                ciclos_mutacao += 1
                index_mut = 0
            MUTACAO = TAXAS_MUTACAO[index_mut]
        if(ciclos_mutacao > N_CICLOS_MUT):
            break
        old_best = individuos[0].fitness

        #ESPALHAMENTO DE GENES
        #espalha_genes_elitismo(individuos,geracao)
        if(TEM_PREDACAO_RANDOMICA and geracao%N_GERACOES_PREDACAO == 0):
            antes = individuos[0]
            for individuo in individuos[1:-1*N_PREDADOS]:
                individuo.cruzamento(individuos[0])
            depois = individuos[0]
            if(antes != depois):
                print("AAAAAAAAAAAAAAAAAAAAAAAA")
            
            #predacao randomica
            for individuo in individuos[-1*N_PREDADOS:]:
                individuo.reset_genes()
        else:
            antes = individuos[0]
            for individuo in individuos[1:]:
                individuo.cruzamento(individuos[0])
            depois = individuos[0]
            if(antes != depois):
                print("AAAAAAAAAAAAAAAAAAAAAAAA")
        
        geracao += 1
    
    plot.plot_fitness(plot_fit, plot_avgfit)
    escreve_log(geracao, individuos)
    exit()