from random import uniform, choices
import controle
from dataclasses import dataclass, field

def test_fitness(individuo):
    return (individuo.Kp + individuo.Ki + individuo.Kd)

def print_bonito(array):
    for item in array:
        print(item)
    print()

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
    def __init__(self) -> None:
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

individuos = []
for i in range(NUMERO_DE_INDIVIDUOS):
    novo_indiv = Individuo()
    individuos.append(novo_indiv)

geracao = 0

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
    if(geracao%100 == 0):
        f = open("logs/" + str(geracao) + ".txt", "w")
        for individuo in individuos:
            f.write(str(individuo) + "\n")
        f.close()
    
    #ESPALHAMENTO DE GENES
    individuos.sort() #coloca o melhor na frente, para nao mata-lo

    for individuo in individuos[1:]:
        individuo.cruzamento(individuos[0])
    
    
    geracao += 1
