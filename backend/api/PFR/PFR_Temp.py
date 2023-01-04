# Script for handling PFR Conversion v. Temperature for an Adiabatic Reactor
#   Takes in:
#       - Lower Temperature Bound
#       - Upper Temperature Bound
#       - Activation Energy
#       - Rate Constant at Reference Temperature
#       - Reference Temperature
#   All other variables are assumed constant

# Example from HW8Q5A
#    Elementary Liquid Phase Reaction (300 K)
#    A + B -> C
#    rate = 0.01*cA*cB

# Importing different libraries
# Library for solving ODEs
import scipy.integrate as integrator
# Library for plotting functions and (in our case) points
import matplotlib.pyplot as plt
# Library for number-related functions and constants
import numpy as np
# Library for math function
import math


# Variable inputs for the user to alter
# Initial temperature to examine - K
Tstart = 300
# End temperature to examine - K
Tend = 1000
# Activation energy - J/mol
Ea_f = 10000
# Rate constant - L^2/(mol^2.min)
k_f0 = 0.00001
# Temperature for original k values - K
T0 = 300


# Permanent Constants
# Temperature for original k values - K
T0 = 300
# Total Concentration - (mol/m^3)
c_T0 = 100  # 0.1 M
# Initial Concentration of A and B
c_A0 = 0.5 * c_T0
c_B0 = 0.5 * c_T0
# Volume of the reactor - m^3
Volume = 0.350  # 350 L
# Initial Volumetric Flowrate - (m^3/s)
volumetric_flowrate = 0.002  # 2 L/s
# Initial Molar Flowrates of A and B
F_A0 = c_A0 * volumetric_flowrate
F_B0 = c_B0 * volumetric_flowrate
# Gas Constant - cal/(mol.K)
R = 1.9872
# Number of elements to plot
num = 101

# ODE function for changing flow rates


def deriv(Volume, F, k):
    """Function to be used in an odesolver

    Parameters
    ----------
    Volume : float
        Value used by the odesolver.  Akin to "t" in normal context and usage.
        Represents the slice of volume of the PFR 
    F : (float, float, float)
        Tuple of three objects representing the current values of:
        (the flowrate of A, the flowrate of B, the flowrate of R)
    k : (float, float)
        A tuple representing the rate constants being used for this particular 
        iteration, especially at the different temperature.  The structure is:
        (k of the forward reaction, k of the reverse reaction)

    Returns
    -------
    list(float)
        A list of floats that represent the change in the flowrates of the 
        different species per volume in the form:
            [dF_A/dV, dF_B/dV]
    """

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
    """Function to act in iteration for each volumetric_flowrate

    Parameters
    ----------
    T : float
        The temperature of the reactor in Kelvin

    Returns
    -------
    list
        List of values that house the initial conditions that were fed into the 
        ODE Solver, followed by the resulting values that were calculated by 
        the ODE Solver
    """
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


# Temperature vector
#   Spans from the start temperature specified to the end temperature
#   specified, separated by the number of points specified (1000)
T_span = np.linspace(Tstart, Tend, num)

# Conversion vector
x = [None] * num

# For loop for iterative function
for i in range(num):
    # Feed in the current temperature to be evaluated
    iter = iterative(T_span[i])
    # Extract the conversion from the end
    x[i] = (iter[0][1] - iter[1][1])/iter[0][1]

# Graphing stuff
plt.plot(T_span, x, 'b', label='Conversion')
plt.legend(loc='best')
plt.xlim(Tstart, Tend)
plt.xlabel('Temperature (K)')
plt.ylim(0, 1)
plt.ylabel('Conversion')
plt.title('PFR-Temperature')
plt.grid()
plt.show()
