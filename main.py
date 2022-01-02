import controle
from dataclasses import dataclass

@dataclass
class Individuo:
    Kp: float
    Ki: float
    Kd: float
    fitness: float

# pega a nota desse tuning (quanto menor, melhor)
Kp = 2
Ki = 1
Kd = 0.8
individuo = Individuo(Kp, Ki, Kd, None)
individuo.fitness = controle.test_tuning(individuo.Kp, individuo.Ki, individuo.Kd)