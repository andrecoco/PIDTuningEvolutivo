import controle

# pega a nota desse tuning (quanto menor, melhor)
Kp = 2
Ki = 1
Kd = 0.8
nota = controle.test_tuning(Kp,Ki,Kd)
