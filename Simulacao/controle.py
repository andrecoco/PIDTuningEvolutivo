import aux_func
import controle_simul

def FOPDT_test_tuning(Kp, Ki, Kd, N_SEGUNDOS = 100):
    temps, pot, set_points = controle_simul.FOPDT_SIMUL(Kp, Ki, Kd, N_SEGUNDOS)
    return aux_func.nota_tecnica(temps, pot, set_points[-1])