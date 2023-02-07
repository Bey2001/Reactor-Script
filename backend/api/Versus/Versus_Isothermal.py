# Script for comparing the resulting conversion under isothermal conditions for identical PFR and CSTRs

# Example from HW8Q5
# Elementary Liquid Phase Reaction (300 K)
# A + B -> C
# rate = 0.01*cA*cB

# Script uses an algebraic solver function.  This does lead to issues with some
# values since the solver itself does not have limitations/constraints on its
# calculations, thus multiple or inaccurate solutions can be reported in the
# graph, leading to some shapes that should not exist and disrupting curves.

# Importing different libraries
# Library for finding 0s to algebraic equations
from scipy.optimize import fsolve
# Importing different libraries
# Library for solving ODEs
import scipy.integrate as integrator
# Library for plotting functions and (in our case) points
import matplotlib.pyplot as plt
# Library for number-related functions and constants
import numpy as np


# Variable inputs for the user to alter
# Volume of the reactor - m^3
volume = 0.350
# Volumetric Flow Rate Parameters - m^3/s
volumetric_flow_low = 0.00001
volumetric_flow_high = 10


# Other numerical values
# Rate Constant - (m^3/mol.s)
k = 0.00001
# Total Concentration - (mol/m^3)
c_T0 = 100
# Number of elements to plot
num = 101


# Values that are calculated from parameters
# Calculation of initial concentrations
c_A0 = 0.5 * c_T0
c_B0 = 0.5 * c_T0
c_C0 = 0
F_A0 = c_A0 * volumetric_flow_low
F_B0 = c_B0 * volumetric_flow_low
F_C0 = c_C0 * volumetric_flow_low
F_T0 = F_A0 + F_B0 + F_C0


# CSTR Business
# Volumetric flow vector
spacetime_start = volume / volumetric_flow_high
spacetime_end = volume / volumetric_flow_low
cstr_spacetime = np.linspace(spacetime_start, spacetime_end, num)

# Conversion vector
cstr_conversion = [None] * num

# For loop for iterative function
for i in range(num):
    # Feed in the current volumetric flowrate
    spacetime = cstr_spacetime[i]
    # Algebraic equation
    def eqn(x): return spacetime - x / (k * c_A0 * (1 - x) ** 2)
    # Initial Guess for fsolve
    initial_guess = 0.99
    # Extract the conversion
    cstr_conversion[i] = fsolve(eqn, initial_guess)[0]


# PFR Business
# ODE function for changing flow rates
initial_conditions = [F_A0, F_B0, F_C0]


def dFdV(volume, F):

    # Unpacking the flowrates at the current volume
    F_A, F_B, F_C = F
    F_T = F_A + F_B + F_C

    volumetric_flowrate = volumetric_flow_low * (F_T / F_T0)
    # Concentration of A
    c_A = F_A/volumetric_flowrate
    # Concentration of B
    c_B = F_B/volumetric_flowrate

    # Rate at this particular point in the volume
    r = k * c_A * c_B

    # List of differentials to be returned
    dFdV = [-r, -r, r]
    return dFdV


v_bounds = [0, volume]
v_span = np.linspace(0, volume, 101)
sol = integrator.solve_ivp(dFdV, v_bounds, initial_conditions,
                           t_eval=v_span, dense_output=True, method='Radau')
F_A, F_B, F_C = sol.y
pfr_conversion = [1 - f_A / F_A0 for f_A in F_A]
v = [volumetric_flow_low * (f_A + f_B + f_C) /
     F_T0 for f_A, f_B, f_C in zip(F_A, F_B, F_C)]
pfr_spacetime = [volume_i / v_i for volume_i, v_i in zip(sol.t, v)]


# Graphing stuff
# Conversion as a function of spacetime
plt.plot(cstr_spacetime, cstr_conversion, 'b', label='CSTR')
plt.plot(pfr_spacetime, pfr_conversion, 'r', label='PFR')
plt.legend(loc='best')
plt.xlim(spacetime_start, spacetime_end)
plt.xlabel('Spacetime')
plt.ylim(0, 1)
plt.ylabel('Conversion')
plt.grid()
plt.show()
