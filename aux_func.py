import numpy as np

# % de erro da temperatura
def erro_medio(temps, set_point):
    temp_media = np.average(temps)
    return (temp_media - set_point)/set_point

# Variabilidade da temperatura (%)
def variabilidade(temps):
    temp_media = np.average(temps)
    desvio_padrao = np.std(temps)
    return (2*desvio_padrao)/temp_media

# Integral do erro absoluto (%)
def iae(temps, set_point):
    erro_absoluto = 0
    for temp in temps:
        erro_absoluto += abs((temp - set_point)/set_point)
    return erro_absoluto

# Numero de vezes em que a temperatura cruzou o setpoint
def cruz_setpoint(temps, set_point):
    temps_compensada = np.array(temps) - set_point
    n_cruzamentos = len(np.where(np.diff(np.sign(temps_compensada)))[0])
    return n_cruzamentos

# Quantidade de movimento na potência (%)
def percurso_pot(pot):
    percurso = 0
    for i in range(len(pot) - 1):
        percurso += abs((pot[i+1] - pot[i])/256)
    return percurso

# Quantidade de vezes que a potência foi diminuida (numero de vezes)
def reversao_pot(pot):
    n_reversoes = 0
    for i in range(len(pot) - 1):
        if(pot[i+1] < pot[i]):
            n_reversoes += 1
    return n_reversoes

# quanto menor a nota, melhor
def nota_tecnica(temps, pot, set_point):
    return (erro_medio(temps, set_point) + 
            variabilidade(temps) + 
            iae(temps, set_point) + 
            cruz_setpoint(temps, set_point) + 
            percurso_pot(pot) + 
            reversao_pot(pot))/6