# Script for handling CSTR Conversion v. Temperature
#   Take in:
#       - Lower Temperature Bound
#       - Upper Temperature Bound
#       - Activation Energy
#       - Rate Constant
#       - Reference Temperature for Rate Constant
#   All other variables are assumed constant

# Example from HW8Q5
#   Elementary Liquid Phase Reaction (300 K)
#   A + B -> C
#   rate = 0.01*cA*cB

# Importing different libraries
# Library for finding 0s to algebraic equations
from scipy.optimize import fsolve
# Library for plotting functions and (in our case) points
import matplotlib.pyplot as plt
# Library for number-related functions and constants
import numpy as np
# Library for math function
import math


# Variable inputs for the user to alter
# Initial Temperature to examine - K
Tstart = 300
# End temperature to examine - K
Tend = 1000
# Forward Activation Energy - J/mol
Ea_f = 10000
# Rate Constant at T0 K - (m^3/mol.s)
k_f0 = 0.01
# Temperature for original k values - K
T0 = 300


# Permanent Constants
# Total Concentration  - (kmol/m^3)
c_T0 = 0.1
# Volume of the reactor - m^3
Volume = 350
# Initial Volumetric Flowrate - m^3/s
volumetric_flowrate = 100
# Number of elements to plot
num = 100
# Gas Constant - J/(mol.K)
R = 8.314


# Values that are calculated from parameters
# Calculation of initial concentrations
#   Initial concentration of A
c_A0 = 0.5 * c_T0


# Temperature vector
T_span = np.linspace(Tstart, Tend, num)

# Conversion vector
x = [None] * num

# For loop for iterative function
for i in range(num):
    # Finding the rate constants
    T = T_span[i]
    # Get the forward reaction rate constant
    k_f = k_f0 * math.exp((Ea_f/R)*((1/T0) - (1/T)))
    # Algebraic equation
    def eqn(x): return Volume/volumetric_flowrate - x/(k_f*c_A0*(1 - x)**2)
    # Initial Guess for fsolve
    initial_guess = 0.99
    # Extract the conversion
    x[i] = fsolve(eqn, initial_guess)

# Graphing stuff
# Conversion as a function of spacetime
plt.plot(T_span, x, 'b', label='Conversion')
plt.legend(loc='best')
plt.xlim(Tstart, Tend)
plt.xlabel('Temperature (K)')
plt.ylim(0, 1)
plt.ylabel('Conversion')
plt.grid()
plt.show()
