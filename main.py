from random import uniform, choices
import controle
from dataclasses import dataclass, field
import os

# DEFINES
## POPULACAO
NUMERO_DE_INDIVIDUOS = 5
MUTACAO_MIN = -0.1
MUTACAO_MAX = 0.1
CHANCE_MUT = 0.5
CHANCE_GENOCIDIO = 0

## INDIVIDUO
MAX_KP = 20
MAX_KI = 20
MAX_KD = 20
MIN_KP = 0.1
MIN_KI = 0.1
MIN_KD = 0.1
PRECISAO = 2  #CASAS DECIMAIS DE PRECISAO

## TESTE
N_MEDIDAS = 120

class Individuo:
    def __init__(self, *args) -> None:
        if (len(args) == 4):
            self.fitness = float(args[3])
            self.Kp = float(args[0])
            self.Ki = float(args[1])
            self.Kd = float(args[2])
        else:
            self.fitness = None
            self.Kp = uniform(MIN_KP, MAX_KP)
            self.Ki = uniform(MIN_KI, MAX_KI)
            self.Kd = uniform(MIN_KD, MAX_KD)

    def __lt__(self, other) -> None:
        return self.fitness < other.fitness

    def __str__(self) -> str:
        return "{},{},{},{}".format(self.Kp, self.Ki, self.Kd, self.fitness)

    def cruzamento(self, parceiro):
        self.Kp = round((parceiro.Kp + self.Kp)/2 + choices([1, 0], [CHANCE_MUT, 1-CHANCE_MUT])[0]*uniform(MUTACAO_MIN, MUTACAO_MAX), PRECISAO)
        self.Ki = round((parceiro.Ki + self.Ki)/2 + choices([1, 0], [CHANCE_MUT, 1-CHANCE_MUT])[0]*uniform(MUTACAO_MIN, MUTACAO_MAX), PRECISAO)
        self.Kd = round((parceiro.Kd + self.Kd)/2 + choices([1, 0], [CHANCE_MUT, 1-CHANCE_MUT])[0]*uniform(MUTACAO_MIN, MUTACAO_MAX), PRECISAO)
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
    if(len(logs) > 0):
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
        for i in range(NUMERO_DE_INDIVIDUOS):
            novo_indiv = Individuo()
            individuos.append(novo_indiv)
    return individuos, geracao

individuos, geracao = inicializa_populacao()

while(True):
    if(geracao == 0):
        for individuo in individuos:
            individuo.fitness = controle.test_tuning(individuo.Kp, individuo.Ki, individuo.Kd, N_MEDIDAS)   
            #individuo.fitness = test_fitness(individuo)
            
    else:
        for individuo in individuos[1:]:
            individuo.fitness = controle.test_tuning(individuo.Kp, individuo.Ki, individuo.Kd, N_MEDIDAS)
            #individuo.fitness = test_fitness(individuo)
    
    #LOGS
    if(geracao%10 == 0):
        escreve_log(geracao, individuos)
    
    #ESPALHAMENTO DE GENES
    individuos.sort() #coloca o melhor na frente, para nao mata-lo

    for individuo in individuos[1:]:
        individuo.cruzamento(individuos[0])
    
    geracao += 1