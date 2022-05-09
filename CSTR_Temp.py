#Script for handling PFR Conversion v. Temperature
#   All other variables are assumed constant

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
# Library for math function
import math



###Variable inputs for the user to alter
# Forward Activation Energy - J/mol
Ea_f = 10000
# Temperature for original k values - K
T0 = 300
# Rate Constant at T0 K - (m^3/mol.s)
k_f0 = 0.01
#Initial Temperature to examine - K
Tstart = 100
#End temperature to examine - K
Tend = 10000

#Total Concentration  - (kmol/m^3)
c_T0 = 0.1

#Volume of the reactor - m^3
Volume = 350

#Initial Volumetric Flowrate - m^3/s
volumetric_flowrate = 100




###Other numerical values
#Number of elements to plot
num = 1000
# Gas Constant - J/(mol.K)
R = 8.314



###Values that are calculated from parameters
#Calculation of initial concentrations
# Initial concentration of A
c_A0 = 0.5 * c_T0
# Initial concentration of B
c_B0 = 0.5 * c_T0



#Function to get the value of k_f at T Kelvin
def k_f_fun(T=T0):
    """Function to calculate the forward k value at a given temperature using 
    the Arrhenius Law

    Parameters
    ----------
    T : float = T0
        The temperature to find k_f for.  The default temperature is whatever 
        is given by the user

    Returns
    -------
    float 
        The value of k_f at temperature T
    """
    k_f =  k_f0 * math.exp((Ea_f/R)*((1/T0) - (1/T)))
    return k_f

#Temperature vector
T_span = np.linspace(Tstart, Tend, num) 

#Conversion vector
x = [None] * num

#For loop for iterative function
for i in range(num):
    #Finding the rate constants
    T = T_span[i]
    #Get the forward reaction rate constant
    k_f = k_f_fun(T)
    #Algebraic equation
    eqn = lambda x : Volume/volumetric_flowrate - x/(k_f*c_A0*(1 - x)**2)
    #Initial Guess for fsolve
    initial_guess = 0.5
    #Extract the conversion
    x[i] = fsolve(eqn, initial_guess)

## Graphing stuff
#Conversion as a function of spacetime
plt.plot(T_span, x, 'b', label='Conversion')    
plt.legend(loc='best')
plt.xlim(Tstart, Tend)
plt.xlabel('Temperature (K)')
plt.ylim(0, 1)
plt.ylabel('Conversion')
plt.grid()
plt.show()