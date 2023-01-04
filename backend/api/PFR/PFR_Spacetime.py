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
# volume of the reactor - m^3
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

# ODE function for changing flow rates


def deriv(volume, F, volumetric_flowrate):
    """Function to be used in an odesolver

    Parameters
    ----------
    volume : float
        Value used by the odesolver.  Akin to "t" in normal context and usage.
        Represents the slice of volume of the PFR 
    F : (float, float, float)
        Tuple of three objects representing the current values of:
        (the flowrate of A, the flowrate of B, the flowrate of R)
    volumetric_flowrate : float
        The volumetric flowrate into the reactor; assumed constant for the 
        purposes of this script.

    Returns
    -------
    list(float)
        A list of floats that represent the change in the flowrates of the 
        different species per volume in the form:
            [dF_A/dV, dF_B/dV]
    """

    # Unpacking the flowrates at the current volume
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
# Function definition replicating ode15s
ode15s = integrator.ode(deriv)
ode15s.set_integrator('vode', method='bdf', order=15, nsteps=1e8)

# Function to house the use of the ODE solver
# Generates the final conversions per iteration using different initial
#   volumetric flowrates


def iterative(volumetric_flowrate):
    """Function to act in iteration for each volumetric_flowrate

    Parameters
    ----------
    volumetric_flowrate : float
        The volumetric flowrate of this particular iteration

    Returns
    -------
    list
        List of values that house the initial conditions that were fed into the 
        ODE Solver, followed by the resulting values that were calculated by 
        the ODE Solver
    """
    # The initial conditions to be fed into the ODE Solver
    F_0 = [volumetric_flowrate*c_A0, volumetric_flowrate*c_B0]
    # Setting the initial conditions for the ODE Solver
    ode15s.set_initial_value(F_0, 0)
    # Setting up the parameters to be fed into the ODE Solver
    ode15s.set_f_params(volumetric_flowrate)
    # Only returns the last iteration of ode15s
    sol = ode15s.integrate(volume)
    array = [F_0, [sol[0], sol[1]]]
    return array


# Volumetric flow vector
#   Spans from the first volumetric flowrate specified by the user to the last,
#   separated by the number of points specified (1000)
volumetric_flow_span = np.linspace(volumetric_flow_low, volumetric_flow_high,
                                   num)

# Conversion vector
x = [None] * num

# For loop for iterative function
for i in range(num):
    # Feed in the current volumetric flowrate
    iter = iterative(volumetric_flow_span[i])
    # Extract the conversion
    x[i] = (iter[0][1] - iter[1][1])/iter[0][1]

# Getting spacetime from the volumes
spacetime = np.divide(volume, volumetric_flow_span)

# Graphing stuff
# Conversion as a function of spacetime
plt.plot(spacetime, x, 'b', label='Conversion')
plt.legend(loc='best')
plt.xlim(volume/volumetric_flow_high, volume/volumetric_flow_low)
plt.xlabel('Spacetime (s)')
plt.ylim(0, 1)
plt.ylabel('Conversion')
plt.title('PFR-Spacetime')
plt.grid()
plt.show()
