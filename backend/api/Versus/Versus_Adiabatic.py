# Script for comparing the resulting conversion under adiabatic conditions for identical PFR and CSTRs
#   Takes in:
#       - Lower Temperature Bound
#       - Upper Temperature Bound
#       - Heat of Reaction
#       - Sum of Specific Heats
#       - Inlet Temperature
#   All other variables are assumed constant
#   Activation energies assumed to be for simplicity's sake

# Example from HW8Q5A
#    Elementary Liquid Phase Reaction (300 K)
#    A + B -> C
#    rate = 0.01*cA*cB

# Importing different libraries
# Library for finding 0s to algebraic equations
from scipy.optimize import fsolve
# Library for solving ODEs
import scipy.integrate as integrator
# Library for plotting functions and (in our case) points
import matplotlib.pyplot as plt
# Library for number-related functions and constants
import numpy as np
# Library for math function
import math


# Variable inputs for the user to alter
# Constants for A
#   Heat of Reaction - (cal/mol)
delta_H_rxn = -10000
# Sum of Specific Heats for all Species
sum_theta_cp = 30
# Inlet Temperature (K)
T0 = 500


# Permanent Constants
# Forward Activation Energy - cal/mol
Ea_f = 10000
# Rate Constant at T0 K - (m^3/mol.s)
k_f0 = 0.00001  # 0.01 L/mol.s
# Total Concentration - (mol/m^3)
c_T0 = 100  # 0.1 M
# Volume of the reactor - m^3
Volume = 0.350  # 350 L
# Volumetric Flow Rate Parameters - m^3/s
volumetric_flow_low = 0.00001
volumetric_flow_high = 0.0001
# Gas Constant - cal/(mol.K)
R = 1.9872
# Number of elements to plot
num_points = 101
num_iter = 5
# Initial Temperature - K
Tstart = 300
# Final temperature - K
Tend = 1000


# Calculation of initial concentrations
# Initial concentration of A
c_A0 = 0.5 * c_T0
# Initial concentration of B
c_B0 = 0.5 * c_T0

# Volumetric flowrate vector
volumetric_flow_span = np.linspace(
    volumetric_flow_low, volumetric_flow_high, num_iter)

# Function to find the intersection between two curves represented as discrete points using linear interpolation
#       Borrowed from https://stackoverflow.com/questions/42464334/find-the-intersection-of-two-curves-given-by-x-y-data-with-high-precision-in


# def interpolated_intercepts(x, y1, y2):
#     """Find the intercepts of two curves, given by the same x data"""

#     def intercept(point1, point2, point3, point4):
#         """Find the intersection between two lines
#         the first line is defined by the line between point1 and point2
#         the first line is defined by the line between point3 and point4
#         each point is an (x,y) tuple.

#         So, for example, you can find the intersection between
#         intercept((0,0), (1,1), (0,1), (1,0)) = (0.5, 0.5)

#         Returns: the intercept, in (x,y) format
#         """

#         def line(p1, p2):
#             A = (p1[1] - p2[1])
#             B = (p2[0] - p1[0])
#             C = (p1[0]*p2[1] - p2[0]*p1[1])
#             return A, B, -C

#         def intersection(L1, L2):
#             D = L1[0] * L2[1] - L1[1] * L2[0]
#             Dx = L1[2] * L2[1] - L1[1] * L2[2]
#             Dy = L1[0] * L2[2] - L1[2] * L2[0]

#             x = Dx / D
#             y = Dy / D
#             return x, y

#         L1 = line([point1[0], point1[1]], [point2[0], point2[1]])
#         L2 = line([point3[0], point3[1]], [point4[0], point4[1]])

#         R = intersection(L1, L2)

#         return R

#     idxs = np.argwhere(np.diff(np.sign(y1 - y2)) != 0)

#     xcs = []
#     ycs = []

#     length = len(x)

#     for idx in idxs:
#         if idx[0] + 1 >= length:
#             break
#         xc, yc = intercept((x[idx], y1[idx]), ((
#             x[idx+1], y1[idx+1])), ((x[idx], y2[idx])), ((x[idx+1], y2[idx+1])))
#         xcs.append(xc)
#         ycs.append(yc)
#     return np.array(xcs), np.array(ycs)

# Look into this https://stackoverflow.com/questions/46909373/how-to-find-the-exact-intersection-of-a-curve-as-np-array-with-y-0/46911822#46911822
def interpolated_intercepts(x, y1, y2):
    y = y1 - y2
    s = np.abs(np.diff(np.sign(y))).astype(bool)
    numerator = np.diff(x)[s]
    denominator = np.abs(y[1:][s]/y[:-1][s]) + 1
    fraction = numerator / denominator
    return x[:-1][s] + fraction


# Iteration function for iterating with different volumetric flowrate
def iter(volumetric_flowrate):

    # Initial Molar Flowrates of A and B
    F_A0 = c_A0 * volumetric_flowrate
    F_B0 = c_B0 * volumetric_flowrate

    # Temperature vector
    T_span = np.linspace(Tstart, Tend, num_points)

    # Conversion vector for the mass balance for the CSTR
    cstr_MB = []
    # Conversion vector for the energy balance for both the PFR and CSTR
    conv_EB = []

    for i in range(num_points):
        # Temperature span
        T = T_span[i]
        # Getting the energy balance values
        conv_EB.append((T - T0)*(-sum_theta_cp/delta_H_rxn))
        # Algebraic equation representing the mass balance

        def eqn(x): return Volume*k_f0*c_A0/volumetric_flowrate - \
            x/(math.exp((Ea_f/R)*((1/T0) - (1/T)))*(1 - x)**2)
        # Initial Guess for fsolve
        initial_guess = 0.99
        # Extract the conversion
        cstr_MB.append(fsolve(eqn, initial_guess)[0])

    cstr_int_x = interpolated_intercepts(
        T_span, np.array(cstr_MB), np.array(conv_EB))
    cstr_int_y = np.interp(cstr_int_x, T_span, conv_EB)

    # PFR stuff

    def deriv(Volume, F, k):
        # Unpacking the flowrates
        F_A, F_B = F
        # Concentration of A
        c_A = F_A/volumetric_flowrate
        # Concentration of B
        c_B = F_B/volumetric_flowrate

        # Rate at this particular point in the volume
        r = k*c_A*c_B

        # List of differentials to be returned
        dFdV = [-r, -r]
        return dFdV

    # Programming of the ODEsolver function
    #   Function definition replicating ode15s
    ode15s = integrator.ode(deriv)
    ode15s.set_integrator('vode', method='bdf', order=15, nsteps=1e8)

    # Function to house the use of the ODE solver
    #   Generates the final conversions per iteration using different temperatures

    def iterative(T):
        # Finding the forward k value
        k_f = k_f0 * math.exp((Ea_f/R)*((1/T0) - (1/T)))
        # Finding the reverse k value
        F_0 = [F_A0, F_B0]
        # Setting the initial conditions for the ODE Solver
        ode15s.set_initial_value(F_0, 0)
        # Setting up the parameters to be fed into the ODE Solver
        ode15s.set_f_params(k_f)
        # Only returns the last iteration of ode15s
        sol = ode15s.integrate(Volume)
        array = [F_0, [sol[0], sol[1]]]
        return array

    # Conversion vector
    pfr_MB = [None] * num_points

    # For loop for iterative function
    for i in range(num_points):
        # Feed in the current temperature to be evaluated
        iter = iterative(T_span[i])
        # Extract the conversion from the end
        pfr_MB[i] = (iter[0][1] - iter[1][1])/iter[0][1]

    pfr_int_x = interpolated_intercepts(
        T_span, np.array(pfr_MB), np.array(conv_EB))
    pfr_int_y = np.interp(pfr_int_x, T_span, conv_EB)

    # plt.plot(T_span, cstr_MB, label="CSTR Mass Balance")
    # plt.plot(T_span, pfr_MB, label="PFR Mass Balance")
    # plt.plot(T_span, conv_EB, label="Energy Balance")
    # plt.show()

    return ((cstr_int_x[0], cstr_int_y[0]), (pfr_int_x[0], pfr_int_y[0]))


cstr_intersections = [[], []]
pfr_intersections = [[], []]

for i in range(num_iter):
    cstr_ints, pfr_ints = iter(volumetric_flow_span[i])
    # print(cstr_ints)
    # print(pfr_ints)
    cstr_intersections[0].append(cstr_ints[0])
    cstr_intersections[1].append(cstr_ints[1])
    pfr_intersections[0].append(pfr_ints[0])
    pfr_intersections[1].append(pfr_ints[1])

# print(cstr_intersections)
# print(pfr_intersections)
# print(cstr_intersections)
# print(pfr_intersections)

# Graphing stuff
spacetime_span = np.divide(Volume, volumetric_flow_span)

fig, ax = plt.subplots()
# Making the Conversion plot
ax.plot(spacetime_span,
        cstr_intersections[1], label='CSTR Exit Conversions', color='blue', marker='o')
ax.plot(spacetime_span,
        pfr_intersections[1], label='PFR Exit Conversions', color='green', marker='o')
# plt.xlim(spacetime_span[-1], spacetime_span[0])
ax.set_xlabel('Spacetime (1/s)')
# plt.ylim(0, 1)
ax.set_ylabel('Conversion', color='blue')

# Making the Exit Temperature Plot
ax2 = ax.twinx()
ax2.plot(spacetime_span,
         cstr_intersections[0], label='CSTR Exit Temp', color='red', marker='x')
ax2.plot(spacetime_span, pfr_intersections[0],
         label='PFR Exit Temp', color='orange', marker='x')
ax2.set_ylabel('Exit Temperature (K)', color='red')
plt.grid()
plt.show()
