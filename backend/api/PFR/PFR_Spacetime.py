# Script for comparing the resulting conversion through a PFR with varying
# spacetime

# Example from HW8Q5
# Elementary Liquid Phase Reaction (300 K)
# A + B -> C
# rate = 0.01*cA*cB

# Importing different libraries
# Library for solving ODEs
import scipy.integrate as integrator
# Library for plotting functions and (in our case) points
import matplotlib.pyplot as plt
# Library for number-related functions and constants
import numpy as np


# Variable inputs for the user to alter
# Volume of the Reactor - m^3
volume = 0.350


# Volumetric Flow Rate - m^3/s
v_0 = 0.0001
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
F_A0 = c_A0 * v_0
F_B0 = c_B0 * v_0
F_C0 = c_C0 * v_0
F_T0 = F_A0 + F_B0 + F_C0

# ODE function for changing flow rates
initial_conditions = [F_A0, F_B0, F_C0]


def dFdV(volume, F):

    # Unpacking the flowrates at the current volume
    F_A, F_B, F_C = F
    F_T = F_A + F_B + F_C

    volumetric_flowrate = v_0 * (F_T / F_T0)
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
conversion = [1 - f_A / F_A0 for f_A in F_A]

v = [v_0 * (f_A + f_B + f_C) / F_T0 for f_A, f_B, f_C in zip(F_A, F_B, F_C)]

spacetime = [volume_i / v_i for volume_i, v_i in zip(sol.t, v)]

# Graphing stuff
# Conversion as a function of spacetime
plt.plot(spacetime, conversion, 'b', label='Conversion')
plt.legend(loc='best')
plt.xlim(spacetime[0], spacetime[-1])
plt.xlabel('Spacetime (s)')
plt.ylim(0, 1)
plt.ylabel('Conversion')
plt.title('PFR-Spacetime')
plt.grid()
plt.show()
