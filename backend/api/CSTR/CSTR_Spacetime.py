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
#Volume of the reactor - m^3
volume = 0.350
#Volumetric Flow Rate Parameters - m^3/s
volumetric_flow_low = 0.00001
volumetric_flow_high = 10



###Other numerical values
#Rate Constant - (m^3/mol.s)
k_f = 0.00001
#Total Concentration - (mol/m^3)
c_T0 = 100
#Number of elements to plot
num = 101



###Values that are calculated from parameters
#Calculation of initial concentrations
c_A0 = 0.5 * c_T0



#Volumetric flow vector
spacetime_start = volume / volumetric_flow_high
spacetime_end = volume / volumetric_flow_low
spacetime_span = np.linspace(spacetime_start, spacetime_end, num) 

#Conversion vector
x = [None] * num

#For loop for iterative function
for i in range(num):
    #Feed in the current volumetric flowrate
    spacetime = spacetime_span[i]
    #Algebraic equation
    eqn = lambda x : spacetime - x / (k_f * c_A0 * (1 - x) ** 2)
    #Initial Guess for fsolve
    initial_guess = 0.99
    #Extract the conversion
    x[i] = fsolve(eqn, initial_guess)[0]

### Graphing stuff
# Conversion as a function of spacetime
plt.plot(spacetime_span, x, 'b', label='Conversion')    
plt.legend(loc='best')
plt.xlim(spacetime_start, spacetime_end)
plt.xlabel('Spacetime')
plt.ylim(0, 1)
plt.ylabel('Conversion')
plt.grid()
plt.show()

# size = 10

# spacetime_print = [[round(j, 5) for j in spacetime_span[i:i+size].tolist()] for i in range(0, len(x), size)]
# for i in spacetime_print:
#     print(', '.join(map(str, i)))
# print('-------------------')
# x_print = [[round(j, 5) for j in x[i:i + size]] for i in range(0, len(x), size)]
# for i in x_print:
#     print(', '.join(map(str, i)))
