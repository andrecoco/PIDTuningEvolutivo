from random import uniform, choices, seed
import controle
import os
import multiprocessing as mp
import numpy as np
import plot

### CONFIGURACOES DO CODIGO ###
## POPULACAO
NUMERO_DE_INDIVIDUOS_POR_THREAD = 10
TAXAS_MUTACAO = [0.25, 0.15, 0.05, 1, 5, 10] #%
#TAXAS_MUTACAO = 6*[1]          #descomentar essa linha caso queira mutacao fixa
LIMITE_CONTADOR = 50            #depois de quantas geracoes sem melhoria alterar a taxa de mutacao
N_CICLOS_MUT = 4                #numero de genocidios antes de parar o algoritmo
CHANCE_MUT = 1                  #chance de se ocorrer mutacao em cada crossover
TEM_GENOCIDIO = True            #define se o genocidio sera utilizado
DELTA = 0.01                    #margem de erro do fitness para considerar que houve melhora
TEM_PREDACAO_RANDOMICA = True   #define se a predacao randomica sera utilizada
N_GERACOES_PREDACAO = 10        #numero de geracoes entre predacoes
N_PREDADOS = 5                  #numero de piores individuos que vao ser predados

## INDIVIDUO
MAX_KP = 20                     #valor maximo para KP
MIN_KP = 0.1                    #valor minimo para KP
MAX_KI = 20                     #valor maximo para KI
MIN_KI = 0.1                    #valor minimo para KI
MAX_KD = 0                      #valor maximo para KD
MIN_KD = 0                      #valor minimo para KD
PRECISAO = 3                    #casas decimais de precisao

## DEFINICOES DA SIMULACAO
N_SEGUNDOS = 100                #tempo simulado
RECUPERA_LOG = False            #define se a simulacao continua de onde parou (a partir dos logs)
LOGGING = True                  #define se os logs com o estado das geracoes e escrito
NUMERO_GERACOES_LOG = 1         #numero de geracoes entre logs

## MULTIPROCESSING
NUMERO_DE_THREADS = 4

### Algumas outras declaracoes (nao configuraveis)
MUTACAO = None #%
RANGE_KP = MAX_KP
RANGE_KI = MAX_KI
RANGE_KD = MAX_KD

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

    # realiza o cruzamento entre o individuo e um parceiro, alem da mutacao dos genes
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
    
    # substitui os genes por valores aleatorios
    def reset_genes(self):
        self.fitness = None
        self.Kp = round(uniform(MIN_KP, MAX_KP), PRECISAO)
        self.Ki = round(uniform(MIN_KI, MAX_KI), PRECISAO)
        self.Kd = round(uniform(MIN_KD, MAX_KD), PRECISAO)

# funcao auxiliar usada para debug
def print_bonito(array):
    for item in array:
        print(item)
    print()

# escreve o arquivo de log
def escreve_log(geracao, individuos):
    f = open("logs/" + str(geracao).zfill(5) + ".txt", "w")
    for individuo in individuos:
        f.write(str(individuo) + "\n")
    f.close()

# recupera o ultimo arquivo de log para continuar a simulacao
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
        return individuos, geracao
    return None, None

# inicializa a populacao do zero, ou a partir de um log antigo
def inicializa_populacao():
    #verifica se existem logs para continuar de onde parou
    individuos, geracao = recupera_log()

    #comeca do zero
    if (individuos is None):
        individuos = []
        geracao = 0
        for i in range(NUMERO_DE_INDIVIDUOS_POR_THREAD*NUMERO_DE_THREADS):
            novo_indiv = Individuo()
            individuos.append(novo_indiv)
    return individuos, geracao

# substitui todos os individuos (com excecao do melhor) por aleatorios
def genocidio(individuos):
    for individuo in individuos[1:]:
        individuo.reset_genes()

# chama a funcao de fitness para os individuos que essa thread e responsavel
def multithread_fitness(inicio, fim, individuos):
    fitness_t = []
    for i in range(inicio, fim):
        individuo = individuos[i]
        fitness_t.append(controle.FOPDT_test_tuning(individuo.Kp, individuo.Ki, individuo.Kd, N_SEGUNDOS))

    return fitness_t


if __name__ == "__main__":
    individuos, geracao = inicializa_populacao()

    threads = [None]*NUMERO_DE_THREADS
    p = mp.Pool(NUMERO_DE_THREADS)

    # para mutacao variavel
    contador = 0
    ciclos_mutacao = 0
    old_best = np.inf
    index_mut = 0
    MUTACAO = TAXAS_MUTACAO[index_mut]

    plot_fit = []
    plot_avgfit = []

    while(True):
        # realiza o teste de fitness dos individuos
        args = []
        for i in range(NUMERO_DE_THREADS):
            args.append((i*NUMERO_DE_INDIVIDUOS_POR_THREAD, (i+1)*NUMERO_DE_INDIVIDUOS_POR_THREAD, individuos))
        mp_solutions = p.starmap(multithread_fitness, args)
        mp_solutions = np.ravel(mp_solutions)
        for i, fit in enumerate(mp_solutions):
            individuos[i].fitness = fit

        individuos.sort() #coloca o melhor na frente, para nao mata-lo

        # armazena dados para o plot ao final
        plot_fit.append(1/(individuos[0].fitness))
        plot_avgfit.append(1/(np.average([ind.fitness for ind in individuos])))

        # log
        if(LOGGING and geracao%NUMERO_GERACOES_LOG == 0):
            escreve_log(geracao, individuos)

        # mutacao dinamica e genocidio
        if(abs(individuos[0].fitness - old_best) <= DELTA):
            contador += 1
        else:
            #print("melhorou na geracao {} :) - mut = {}%".format(geracao, MUTACAO))
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

        # espalhamento dos genes
        if(TEM_PREDACAO_RANDOMICA and geracao%N_GERACOES_PREDACAO == 0):
            for individuo in individuos[1:-1*N_PREDADOS]:
                individuo.cruzamento(individuos[0])
            
            #predacao randomica
            for individuo in individuos[-1*N_PREDADOS:]:
                individuo.reset_genes()
        else:
            for individuo in individuos[1:]:
                individuo.cruzamento(individuos[0])

        geracao += 1

    plot.plot_fitness(plot_fit, plot_avgfit)
    plot.plot_params_from_log()
    escreve_log(geracao, individuos)
    exit()