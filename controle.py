import serial
import time
import numpy as np
import plot
import aux_func

def test_tuning(Kp, Ki, Kd, N_MEDIDAS=60):
    N_MEDIDAS = 60

    com = serial.Serial('COM4', 9600, timeout=1) # Setando timeout 1s para a conexao

    time.sleep(2) #se nao esperar o write nao funciona
    data = '{}, {}, {}, {}'.format(Kp, Ki, Kd, N_MEDIDAS)
    com.write(bytearray(data.encode()))

    #com.readline()
    #KPI = str(com.readline()).replace("\r\n","")
    #print(KPI) #debug print

    set_point = None
    temps = []
    pot = []

    for i in range(N_MEDIDAS):
        VALUE_SERIAL=str(com.readline()).replace("\\r\\n","")[3:-1]
        while(VALUE_SERIAL == ""): #waiting for it to cool down or heat up
            VALUE_SERIAL=str(com.readline()).replace("\\r\\n","")[3:-1]
        parsed_values = VALUE_SERIAL.split(',')
        print(i, ' - ', parsed_values)
        set_point = float(parsed_values[0])
        temps.append(float(parsed_values[1]))
        pot.append(float(parsed_values[2]))
    com.close()

    #print("TESTES")
    #print(temps)
    #print(pot)
    #print(len(temps))
    #print(len(pot))

    #plot.plot_graph(temps, pot, N_MEDIDAS, Kp, Ki, Kd, set_point)

    nota_tecnica = aux_func.nota_tecnica(temps, pot, set_point)
    print(nota_tecnica)
    return nota_tecnica