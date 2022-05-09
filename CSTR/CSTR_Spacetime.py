#Script for comparing the resulting conversion through a PFR with varying 
# spacetime

#Example from HW8Q5
# Elementary Liquid Phase Reaction (300 K)
# A + B -> C
# rate = 0.01*cA*cB

#Script uses an algebraic solver function.  This does lead to issues with some 
# values since the solver itself does not have limitations/constraints on its 
# calculations, thus multiple or inaccurate solutions can be reported in the 
# graph, leading to some shapes that should not exist and disrupting curves.

###Importing different libraries
# Library for finding 0s to algebraic equations
from scipy.optimize import fsolve
# Library for plotting functions and (in our case) points
import matplotlib.pyplot as plt
# Library for number-related functions and constants
import numpy as np



###Variable inputs for the user to alter
#Rate Constant - (m^3/mol.s)
k_f = 0.00001

#Total Concentration - (kmol/m^3)
c_T0 = 0.1

#Volume of the reactor - m^3
Volume = 350

#Volumetric Flow Rate Parameters - m^3/s
volumetric_flow_low = 0.001
volumetric_flow_high = 20



###Other numerical values
#Number of elements to plot
num = 1000



###Values that are calculated from parameters
#Calculation of initial concentrations
c_A0 = 0.5 * c_T0
c_B0 = 0.5 * c_T0



#Volumetric flow vector
volumetric_flow_span = np.linspace(volumetric_flow_low, volumetric_flow_high, num) 

#Conversion vector
x = [None] * num

#For loop for iterative function
for i in range(num):
    #Feed in the current volumetric flowrate
    v = volumetric_flow_span[i]
    #Algebraic equation
    eqn = lambda x : Volume/v - x/(k_f*c_A0*(1 - x)**2)
    #Initial Guess for fsolve
    initial_guess = 0.5
    #Extract the conversion
    x[i] = fsolve(eqn, initial_guess)

#Getting spacetime from the volumes
spacetime = np.divide(Volume, volumetric_flow_span)

## Graphing stuff
#Conversion as a function of spacetime
plt.plot(spacetime, x, 'b', label='Conversion')    
plt.legend(loc='best')
plt.xlim(Volume/volumetric_flow_high, Volume/volumetric_flow_low)
plt.xlabel('Spacetime')
plt.ylim(0, 1)
plt.ylabel('Conversion')
plt.grid()
plt.show()