#Script for handling CSTR Conversion v. Temperature
#   All other variables are assumed constant
#   Activation energies assumed to be for simplicity's sake

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
#Constants for A
#   Heat of formation of A - (cal/mol)
delta_H_A = -20000
#   Specfic heat of A - (cal/mol)
cp_A = 15
#Constants for B
#   Heat of formation of B - (cal/mol)
delta_H_B = -15000
#   Specific heat of B - (cal/mol)
cp_B = 15
#Constants for C
#   Heat of formation of C - (cal/mol)
delta_H_C = -41000
#   Specific heat of C - (cal/mol)
cp_C = 30

# Forward Activation Energy - cal/mol
Ea_f = 10000
# Temperature for original k values - K
T0 = 300
# Rate Constant at T0 K - (m^3/mol.s)
k_f0 = 0.00001

#Initial Temperature - K
Tstart = 300
#Final temperature - K
Tend = 500

#Total Concentration - (mol/m^3)
c_T0 = 100

#Volume of the reactor - m^3
Volume = 0.350

#Initial Volumetric Flowrate - (m^3/s)
volumetric_flowrate = 0.002



###Other numerical values
#Number of elements to plot
num = 1000
# Gas Constant - cal/(mol.K)
R = 1.9872



###Values that are calculated from parameters
#Total heat of reaction
delta_H_r = delta_H_C - delta_H_A - delta_H_B
#Change in specific heat capacity of all species
delta_cp = cp_C - cp_A - cp_B
#Calculation of initial concentrations
# Initial concentration of A
c_A0 = 0.5 * c_T0
# Initial concentration of B
c_B0 = 0.5 * c_T0
#Summing up all the heat capacities of species in the feed
sum_theta_cp = cp_A + cp_B



#Function to get the temperature based on the conversion from the energy balance
def conversion_fun(T):
    """Function to return the concentration that corresponds to the given T from the energy balance
    
    Parameters
    ----------
    T : float
        The temperature at which the conversion must be found
    
    Returns
    -------
    float
        The conversion found at T from the energy balance"""
    conversion = (T - T0)*(-sum_theta_cp/delta_H_r)
    return conversion

#Temperature vector
T_span = np.linspace(Tstart, Tend, num) 

#Conversion vectors
# Conversion vector for the mass balance
x_MB = [None] * num
# Conversion vector for the energy balance
x_EB = [None] * num

for i in range(num):
    #Temperature span
    T = T_span[i]
    #Getting the energy balance values
    x_EB[i] = conversion_fun(T)
    #Algebraic equation representing the mass balance
    eqn = lambda x : Volume*k_f0*c_A0/volumetric_flowrate - x/(math.exp((Ea_f/R)*((1/T0) - (1/T)))*(1 - x)**2)
    #Initial Guess for fsolve
    initial_guess = 0.9
    #Extract the conversion
    x_MB[i] = fsolve(eqn, initial_guess)

## Graphing stuff
#Conversion as a function of spacetime
plt.plot(T_span, x_MB, 'b', label='Material Balance')    
plt.plot(T_span, x_EB, 'r', label='Energy Balance')
plt.legend(loc='best')
plt.xlim(Tstart, Tend)
plt.xlabel('Temperature (K)')
plt.ylim(0, 1)
plt.ylabel('Conversion')
plt.grid()
plt.show()