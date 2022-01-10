from random import uniform, choices
import controle
from dataclasses import dataclass, field
import os
import time
import multiprocessing as mp
import numpy as np

# DEFINES
## POPULACAO
NUMERO_DE_INDIVIDUOS_POR_THREAD = 10
MUTACAO = None #%
TAXAS_MUTACAO = [0.25, 0.15, 0.05, 1, 5, 10] #%
CHANCE_MUT = 1
CHANCE_GENOCIDIO = 0
DELTA = 0.01
## MUT_MIN 0.01 (0.05%)
## MUT_MAX 5    (10%)
## COMECA 0.25%
## cai para 0.15%
## cai para 0.05%
## vai para 0.5%
## vai para 1%
## vai para 5%
## vai para 10%
## genocidio

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
N_MEDIDAS = 600 #Arduino
N_SEGUNDOS = 100 #Simulacao
RECUPERA_LOG = False

## MULTITHREADING
NUMERO_DE_THREADS = 4

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
        return individuos, geracao
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

def genocidio(individuos):
    for individuo in individuos[1:]:
        individuo.reset_genes()

def multithread_fitness(inicio, fim, individuos):
    fitness_t = []
    for i in range(inicio, fim):
        individuo = individuos[i]
        fitness_t.append(controle.FOPDT_test_tuning(individuo.Kp, individuo.Ki, individuo.Kd, N_SEGUNDOS))

    return fitness_t


if __name__ == "__main__":
    
    #for i in range(1):
    #    print(controle.FOPDT_test_tuning(19.997,2.125, 0, N_SEGUNDOS))  
    #    print(controle.FOPDT_test_tuning(7.403, 3.126, 0, N_SEGUNDOS))  
    #exit()

    individuos, geracao = inicializa_populacao()

    threads = [None]*NUMERO_DE_THREADS
    inicio = time.time()
    p = mp.Pool(NUMERO_DE_THREADS)

    # Mutacao variavel
    contador = 0 #pra mutacao variavel
    n_genocidios = 0
    old_best = np.inf
    index_mut = 0
    MUTACAO = TAXAS_MUTACAO[index_mut]

    while(True):
        #print("main - ", individuos[0].Kp, individuos[0].Ki, individuos[0].Kd)
        #print(geracao)
        if(geracao == 0):
            '''for individuo in individuos:
                #individuo.fitness = controle.test_tuning(individuo.Kp, individuo.Ki, individuo.Kd, N_MEDIDAS)   
                #individuo.fitness = test_fitness(individuo)
                #individuo.fitness = controle.SIMULtest_tuning(individuo.Kp, individuo.Ki, individuo.Kd, N_MEDIDAS)
                individuo.fitness = controle.FOPDT_test_tuning(individuo.Kp, individuo.Ki, individuo.Kd, N_MEDIDAS)'''
            
            args = []
            for i in range(NUMERO_DE_THREADS):
                args.append((i*NUMERO_DE_INDIVIDUOS_POR_THREAD, (i+1)*NUMERO_DE_INDIVIDUOS_POR_THREAD, individuos))
            mp_solutions = p.starmap(multithread_fitness, args)
            mp_solutions = np.ravel(mp_solutions)
            for i, fit in enumerate(mp_solutions):
                individuos[i].fitness = fit

        else:
            '''for individuo in individuos[1:]:
                #individuo.fitness = controle.test_tuning(individuo.Kp, individuo.Ki, individuo.Kd, N_MEDIDAS)
                #individuo.fitness = test_fitness(individuo)
                #individuo.fitness = controle.SIMULtest_tuning(individuo.Kp, individuo.Ki, individuo.Kd, N_MEDIDAS)
                individuo.fitness = controle.FOPDT_test_tuning(individuo.Kp, individuo.Ki, individuo.Kd, N_MEDIDAS)'''
            
            args = []
            for i in range(NUMERO_DE_THREADS):
                args.append((i*NUMERO_DE_INDIVIDUOS_POR_THREAD, (i+1)*NUMERO_DE_INDIVIDUOS_POR_THREAD, individuos))
            mp_solutions = p.starmap(multithread_fitness, args)
            mp_solutions = np.ravel(mp_solutions)
            for i, fit in enumerate(mp_solutions):
                individuos[i].fitness = fit

        individuos.sort() #coloca o melhor na frente, para nao mata-lo

        #LOGS
        if(geracao%50 == 0):
            fim = time.time()
            print("Tempo: ", fim - inicio)
            inicio = time.time()
            escreve_log(geracao, individuos)

        # MUTACAO DINAMICA
        if(geracao%2 == 0):
            #ve se melhorou nas ultimas 2 geracoes
            if(abs(individuos[0].fitness - old_best) <= DELTA):
                contador += 1
                #print("contador++")
            else: #se melhorou
                #print("melhorou:)")
                contador = 0
                index_mut = 0
                MUTACAO = TAXAS_MUTACAO[index_mut]
                n_genocidios = 0
            
            if(contador >= 20):
                contador = 0
                index_mut += 1
                if(index_mut >= len(TAXAS_MUTACAO)):
                    #print("genocidio :(")
                    genocidio(individuos)
                    n_genocidios += 1
                    index_mut = 0
                MUTACAO = TAXAS_MUTACAO[index_mut]
            if(n_genocidios >= 5):
                #print("cabo")
                break
            old_best = individuos[0].fitness

        #ESPALHAMENTO DE GENES    
        antes = individuos[0]
        #print(individuos[0])
        for individuo in individuos[1:]:
            individuo.cruzamento(individuos[0])
        depois = individuos[0]
        if(antes != depois):
            print("AAAAAAAAAAAAAAAAAAAAAAAA")
        
        geracao += 1
    
    escreve_log(geracao, individuos)
    exit()