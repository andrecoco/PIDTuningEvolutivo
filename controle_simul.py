import numpy as np # Acho que da pra substituir
import matplotlib.pyplot as plt # Plot - nao_precisa
from scipy.integrate import odeint # EDO - precisa
import time
from numba import jit

NOISE = False
SET_POINT = 80
OUTPUT_LIMIT = 255
TEMP_LIMIT = 200

'''t_model = None #substitui self.t
Gain_model = None #substitui self.Gain
TimeConstant_model = None #substitui self.TimeConstant
DeadTime_model = None #substitui self.DeadTime
Bias_model = None #substitui self.Bias
CV_model = None #substitui self.CV'''

#@jit
def calc(PV,ts):
    #print(t_model, DeadTime_model, Bias_model, Gain_model)
    #time.sleep(1)
    #global t_model, DeadTime_model, Bias_model, Gain_model, TimeConstant_model, CV_model
    if (t_model-DeadTime_model) <= 0:
        um=0
    else:
        um=CV_model[t_model-int(DeadTime_model)]

    dydt = (-(PV-Bias_model) + Gain_model * um)/TimeConstant_model
    return dydt

def _clamp(value, limits):
    lower, upper = limits
    if value is None:
        return None
    elif (upper is not None) and (value > upper):
        return upper
    elif (lower is not None) and (value < lower):
        return lower
    return value

class PID(object):
    
    def __init__(
        self,
        Kp=1.0,
        Ki=0.1,
        Kd=0.01,
        setpoint=SET_POINT,
        output_limits=(0, OUTPUT_LIMIT),
   
    ):

        self.Kp, self.Ki, self.Kd = Kp, Ki, Kd
        self.setpoint = setpoint

        self._min_output, self._max_output = 0, OUTPUT_LIMIT

        self._proportional = 0
        self._integral = 0
        self._derivative = 0

        self.output_limits = output_limits
        self._last_eD = 0
        self._lastCV = 0
        self._d_init = 0

        self.reset()


    def __call__(self,PV=0,SP=0):
            # PID calculations            
            #P term
            e = SP - PV        
            self._proportional = self.Kp * e

            #I Term
            if self._lastCV<OUTPUT_LIMIT and self._lastCV >0:        
                self._integral += self.Ki * e

            #D term
            eD=-PV 
            self._derivative = self.Kd*(eD - self._last_eD)

            #init D term 
            if self._d_init==0:
                self._derivative=0
                self._d_init=1

            #Controller Output
            CV = self._proportional + self._integral + self._derivative
            CV = _clamp(CV, self.output_limits)

            # update stored data for next iteration
            self._last_eD = eD
            self._lastCV=CV

            return CV
        

    @property
    def components(self):

        return self._proportional, self._integral, self._derivative

    @property
    def tunings(self):

        return self.Kp, self.Ki, self.Kd

    @tunings.setter
    def tunings(self, tunings):        
        self.Kp, self.Ki, self.Kd = tunings
    
    @property
    def output_limits(self): 
        return self._min_output, self._max_output

    @output_limits.setter
    def output_limits(self, limits):
        
        if limits is None:
            self._min_output, self._max_output = 0, OUTPUT_LIMIT
            return

        min_output, max_output = limits

        self._min_output = min_output
        self._max_output = max_output

        self._integral = _clamp(self._integral, self.output_limits)
        

    def reset(self):
        #Reset
        self._proportional = 0
        self._integral = 0
        self._derivative = 0
        self._integral = _clamp(self._integral, self.output_limits)
        self._last_eD=0
        self._lastCV=0
        self._last_eD =0
        
class FOPDTModel(object):
    
    def __init__(self, PlantParams, ModelData):
        global t_model, Gain_model, TimeConstant_model, DeadTime_model, Bias_model, CV_model
        t_model, CV_model= PlantParams
        Gain_model, TimeConstant_model, DeadTime_model, Bias_model = ModelData

    def update(self,PV, ts):

        y = odeint(calc, PV, ts)

        return y[-1]

def refresh(ikp, iki, ikd, igain, itau, ideadtime, size, noise, PLOT_GRAPH = False):

    rangesize = size

    #setup time intervals
    t = np.arange(start=0, stop=rangesize, step=1)

    #Setup data arrays
    SP = np.zeros(len(t)) 
    PV = np.zeros(len(t))
    CV = np.zeros(len(t))
    pterm = np.zeros(len(t))
    iterm = np.zeros(len(t))
    dterm = np.zeros(len(t))
    noise=np.resize(noise, len(t))
    #noise= np.zeros(len(t)) #no noise
    
    #defaults
    ibias=10
    startofstep=1

    #Packup data
    PIDGains=(ikp,iki,ikd)
    ModelData=(igain,itau,ideadtime,ibias)
    PlantParams=(t, CV)

    #PID Instantiation
    pid = PID(ikp, iki, ikd, SP[0])
    pid.output_limits = (0, OUTPUT_LIMIT)
    pid.tunings=(PIDGains)

    #plant Instantiation
    plant=FOPDTModel(PlantParams, ModelData)

    #Start Value
    PV[0]=ibias+noise[0]
    
    #Loop through timestamps
    for i in t:        
        if i<(len(t)-1):
            SP[i] = 0 if i < startofstep else SET_POINT
            #Find current controller output
            CV[i]=pid(PV[i], SP[i])               
            ts = [t[i],t[i+1]]
            #Send step data
            global t_model
            t_model,plant.CV=i,CV
            #Find calculated PV
            PV[i+1] = plant.update(PV[i],ts)
            PV[i+1]+=noise[i]
            #Limit PV
            if PV[i+1]>TEMP_LIMIT:
                PV[i+1]=TEMP_LIMIT
            if PV[i+1]<ibias:
                PV[i+1]=ibias
            #Store indiv. terms
            pterm[i],iterm[i],dterm[i]=pid.components
        else:
            #cleanup endpoint
            SP[i]=SP[i-1]
            CV[i]=CV[i-1]
            pterm[i]=pterm[i-1]
            iterm[i]=iterm[i-1]
            dterm[i]=dterm[i-1]
        #itae = 0 if i < startofstep else itae+(i-startofstep)*abs(SP[i]-PV[i])
            
    #Display itae value    
    #itae_text.set(round(itae/len(t),2)) #measure PID performance
    if(PLOT_GRAPH):
        plt.figure()    
        plt.subplot(2, 1, 1) 
        plt.plot(t,SP, color="blue", linewidth=2, label='SP')
        plt.plot(t,CV,color="darkgreen",linewidth=2,label='CV')
        plt.plot(t,PV,color="red",linewidth=2,label='PV')    
        plt.ylabel('EU')    
        #plt.suptitle("ITAE: %s" % round(itae/len(t),2))        
        plt.title("Kp:%s   Ki:%s  Kd:%s" % (ikp, iki, ikd),fontsize=10)
        plt.legend(loc='best')

        plt.subplot(2,1,2)
        plt.plot(t,pterm, color="lime", linewidth=2, label='P Term')
        plt.plot(t,iterm,color="orange",linewidth=2,label='I Term')
        plt.plot(t,dterm,color="purple",linewidth=2,label='D Term')        
        plt.xlabel('Time [seconds]')
        plt.legend(loc='best')
        plt.show()

    return PV, CV, SP 

#EntryPoint
def FOPDT_SIMUL(ikp, iki, ikd, N_SEGUNDOS, igain = 0.42, itau = 30, ideadtime = 0.1):
    # Some Definitions
    #Random Noise between -0.5 and 0.5, same set used for each run. Created once at runtime.
    size = N_SEGUNDOS
    if(NOISE):
        np.random.seed(0)
        noise = np.random.rand(size)*2
        noise -= 0.1
    else:
        noise = [0]*size
    return refresh(ikp, iki, ikd, igain, itau, ideadtime, size, noise, PLOT_GRAPH=False)