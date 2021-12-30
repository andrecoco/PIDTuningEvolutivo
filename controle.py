import serial
import time
import matplotlib.pyplot as plt
import numpy as np

N_MEDIDAS = 60
Kp = 2
Ki = 0.5
Kd = 0.3

com = serial.Serial('COM4', 9600, timeout=1) # Setando timeout 1s para a conexao

time.sleep(2) #se nao esperar o write nao funciona
tunings = '{}, {}, {}'.format(Kp, Ki, Kd)
com.write(bytearray(tunings.encode()))

com.readline()
KPI = str(com.readline()).replace("\r\n","")
#print(KPI) #debug print

set_point = None
temps = []
pot = []

for i in range(N_MEDIDAS):
    VALUE_SERIAL=str(com.readline()).replace("\\r\\n","")[3:-1]
    while(VALUE_SERIAL == ""): #waiting for it to cool down
        VALUE_SERIAL=str(com.readline()).replace("\\r\\n","")[3:-1]
    parsed_values = VALUE_SERIAL.split(',')
    print(parsed_values)
    set_point = parsed_values[0]
    temps.append(float(parsed_values[1]))
    pot.append(float(parsed_values[2]))
com.close()

print("TESTES")
print(temps)
print(pot)
#print(len(temps))
#print(len(pot))

# Data for plotting
t = np.linspace(0, N_MEDIDAS//2, N_MEDIDAS)

color = 'tab:red'
fig, ax1 = plt.subplots()
ax1.plot(t, temps, label = 'temp', color=color)
ax1.set_ylabel('temp', color=color)
ax1.set(xlabel='tempo (s)',
       title='Kp = {}, Ki = {}, Kd = {}, Setpoint = {}'.format(Kp, Ki, Kd, set_point))
#ax1.set_ylim([50, 1.1*float(set_point)])
ax1.grid()

color = 'tab:blue'  
ax2 = ax1.twinx()
ax2.plot(t, pot, label = 'pot', color=color)
ax2.set_ylabel('pot', color=color)
#ax2.set_ylim([0, 1.1*256])

plt.tight_layout()
plt.legend()
plt.show()