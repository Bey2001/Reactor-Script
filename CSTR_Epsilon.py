#Script for handling PFR Conversion v. Temperature
#   All other variables are assumed constant
#   Activation energies assumed to be for simplicity's sake

#Example from HW8Q5
# Elementary Liquid Phase Reaction (300 K)
# A + nB -> C
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
# Rate Constant at 300 K - (m^3/mol.s)
k_f = 1
###Coefficient Parameters
coefficient_start = 1
coefficient_end = 4
#Total Concentration - (kmol/m^3)
c_T0 = 0.1
#Volume of the reactor - m^3
Volume = 350
#Initial Volumetric Flowrate - m^3/s
volumetric_flowrate = 100



###Other numerical values
#Number of elements to plot
num = 1000



###Values that are calculated from parameters
#Calculation of initial concentrations
c_A0 = 0.5 * c_T0
c_B0 = 0.5 * c_T0



#Temperature vector
coefficient_span = np.linspace(coefficient_start, coefficient_end, num) 

#Conversion vector
x = [None] * num

#For loop for iterative function
for i in range(num):
    n = coefficient_span[i]
    #Algebraic equation
    eqn = lambda x : Volume/volumetric_flowrate - x/(k_f*(c_A0**(n - 1))*(np.sign(1 - x)*(np.abs((1 - x))**(n + 1))))
    #Initial Guess for fsolve
    initial_guess = 0.5
    #Extract the conversion
    x[i] = fsolve(eqn, initial_guess)

## Graphing stuff
#Conversion as a function of spacetime
plt.plot(coefficient_span, x, 'b', label='Conversion')    
plt.legend(loc='best')
plt.xlim(coefficient_start, coefficient_end)
plt.xlabel('Coefficient of B')
plt.ylim(0, 1)
plt.ylabel('Conversion')
plt.grid()
plt.show()