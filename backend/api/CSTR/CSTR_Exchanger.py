# Script for handling CSTR Conversion v. Temperature
#   Takes in:
#       - Lower Temperature Bound
#       - Upper Temperature Bound
#       - Heat Transfer Coefficient (U)
#       - Area of Heat Transfer (A)
#       - Surface of Temperature (T_Surface)
#   All other variables are assumed constant
#   Activation energies assumed to be for simplicity's sake

# Example from HW8Q5
# Elementary Liquid Phase Reaction (300 K)
# A + B -> C
# rate = 0.01*cA*cB

# Importing different libraries
# Library for plotting functions and (in our case) points
import matplotlib.pyplot as plt
# Library for number-related functions and constants
import numpy as np


# Variable inputs for the user to alter
# Initial temperature  - K
Tstart = 300
# End temperature - K
Tend = 500
# Heat Exchanger parameters
# Overall heat transfer coefficient - (W/m^2.K)
U = 630
# Area of heat exchange - (m^2)
A = 0.00033
# Surface Temperature - K
T_A = 330


# Permanent Constants
# Forward Activation Energy - cal/mol
Ea_f = 10000
# Temperature for original k values - K
T0 = 300
# Rate constant at T0 K - (m^3/mol.s)
k_f0 = 0.00001
# Constants for A
#   Heat of formation of A - (cal/mol)
delta_H_A = -20000
#   Specfic heat of A - (cal/mol)
cp_A = 15
# Constants for B
#   Heat of formation of B - (cal/mol)
delta_H_B = -15000
#   Specific heat of B - (cal/mol)
cp_B = 15
# Constants for C
#   Heat of formation of C - (cal/mol)
delta_H_C = -41000
#   Specific heat of C - (cal/mol)
cp_C = 30
# Total Concentration (mol/m^3)
c_T0 = 100
# Volume of the reactor - m^3
Volume = 0.350
# Initial Volumetric Flowrate (m^3/s)
volumetric_flowrate = 0.002
# Gas Constant - cal/(mol.K)
R = 1.9872
# Number of elements to plot
num = 101


# Values that are calculated from parameters
# Total heat of reaction
delta_H_r = delta_H_C - delta_H_A - delta_H_B
# Difference in the heat capacities of the chemical species
delta_cp = cp_C - cp_A - cp_B
# Calculation of initial concentrations
#   Initial concentration of A
c_A0 = 0.5 * c_T0
# Initial Molar Flowrate (mol/s)
F_A0 = volumetric_flowrate*c_A0
# Summing up all the heat capacities of species in the feed
sum_theta_cp = cp_A + cp_B


# Mass Balance vectors - Length 101 to have clean numbers
# These are actually constant, regardless of values input by user
#   Conversion vector for the mass balance
#   - Constant across the temperature, regardless of thermodynamic properties
#   - Calculated by using the original CSTR_Adiabatic script from 300 to 1000K
x_MB = [0.075, 0.103, 0.138, 0.177, 0.222, 0.269, 0.319, 0.368, 0.417, 0.463,
        0.507, 0.549, 0.587, 0.622, 0.653, 0.683, 0.709, 0.733, 0.754, 0.774,
        0.791, 0.807, 0.822, 0.835, 0.847, 0.858, 0.867, 0.876, 0.884, 0.892,
        0.899, 0.905, 0.911, 0.916, 0.921, 0.925, 0.929, 0.933, 0.936, 0.94,
        0.943, 0.946, 0.948, 0.951, 0.953, 0.955, 0.957, 0.959, 0.961, 0.962,
        0.964, 0.965, 0.967, 0.968, 0.969, 0.97, 0.971, 0.972, 0.973, 0.974,
        0.975, 0.976, 0.977, 0.977, 0.978, 0.979, 0.979, 0.98, 0.98, 0.981,
        0.982, 0.982, 0.983, 0.983, 0.983, 0.984, 0.984, 0.985, 0.985, 0.985,
        0.986, 0.986, 0.986, 0.987, 0.987, 0.987, 0.988, 0.988, 0.988, 0.988,
        0.989, 0.989, 0.989, 0.989, 0.989, 0.99, 0.99, 0.99, 0.99, 0.99,
        0.991]
#   Temperature vector for the mass balance
T_MB = [300.0, 307.0, 314.0, 321.0, 328.0, 335.0, 342.0, 349.0, 356.0, 363.0,
        370.0, 377.0, 384.0, 391.0, 398.0, 405.0, 412.0, 419.0, 426.0, 433.0,
        440.0, 447.0, 454.0, 461.0, 468.0, 475.0, 482.0, 489.0, 496.0, 503.0,
        510.0, 517.0, 524.0, 531.0, 538.0, 545.0, 552.0, 559.0, 566.0, 573.0,
        580.0, 587.0, 594.0, 601.0, 608.0, 615.0, 622.0, 629.0, 636.0, 643.0,
        650.0, 657.0, 664.0, 671.0, 678.0, 685.0, 692.0, 699.0, 706.0, 713.0,
        720.0, 727.0, 734.0, 741.0, 748.0, 755.0, 762.0, 769.0, 776.0, 783.0,
        790.0, 797.0, 804.0, 811.0, 818.0, 825.0, 832.0, 839.0, 846.0, 853.0,
        860.0, 867.0, 874.0, 881.0, 888.0, 895.0, 902.0, 909.0, 916.0, 923.0,
        930.0, 937.0, 944.0, 951.0, 958.0, 965.0, 972.0, 979.0, 986.0, 993.0,
        1000.0]

# Energy Balance vectors
# Simple linear calculations
T_EB = np.linspace(Tstart, Tend, num)
x_EB = [(U*A*(T_A - T) - F_A0*sum_theta_cp*(T - T0)) /
        (F_A0*(delta_cp*(T - T0) + delta_H_r)) for T in T_EB]


# Graphing stuff
plt.plot(T_MB, x_MB, 'b', label='Material Balance')
plt.plot(T_EB, x_EB, 'r', label='Energy Balance')
plt.legend(loc='best')
plt.xlim(Tstart, Tend)
plt.xlabel('Temperature (K)')
plt.ylim(0, 1)
plt.ylabel('Conversion')
plt.grid()
plt.show()
