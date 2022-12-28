#Script for handling PFR Conversion v. Epsilon
#   Only thing that changes is the value n in the reaction's chemical equation
#       Also affects the rate equation, since the situation is assumed to be #          elementary

#Example from HW4Q1
# Elementary Liquid Phase Reaction
# A + 2B <-> nR
# -rA = -(1/2)rB = 12.5*cA*cB^2 - 1.5*cR^n

#Script uses a numerical solution to the differential equations that define the 
# problem, finding the change in the flowrate per change in volume at multiple 
# points over multiple iterations.  The resulting array created from iterating 
# this process for various volumes is then plotted against the coefficient of R
# that was used for that specific iteration.

###Importing different libraries
# Library for solving ODEs
import scipy.integrate as integrator
# Library for plotting functions and (in our case) points
import matplotlib.pyplot as plt
# Library for number-related functions and constants
import numpy as np



###Variable inputs for the user to alter
#Rate Constants
# Forward reaction rate constant - L^2/(mol^2.min)
k_f = 12.5
# Reverse reaction rate constant - L/(mol.min)
k_r = 1.5

#Initial Concentrations - mol/L
c_A0 = 2.8
c_B0 = 1.6

#Volumetric Flowrate - L/min
volumetric_flowrate = 100

#Volume parameter - L
Volume_total = 6

#Coefficient of R in the equation
coefficient_start = 1
coefficient_end = 4



###Other numerical values
#Dummy variable to hold 0 (the lower bound of integration) - L
Volume_0 = 0
#Number of elements to plot
num = (coefficient_end - coefficient_start)*5

#ODE function for changing flow rates
def deriv(Volume, F, n):
    """Function to be used in an odesolver
    
    Parameters
    ----------
    Volume : float
        Value used by the odesolver.  Akin to "t" in normal context and usage.
        Represents the slice of volume of the PFR 
    F : (float, float, float)
        Tuple of three objects representing the current values of:
        (the flowrate of A, the flowrate of B, the flowrate of R)
    n : float
        The coefficient of R in the chemical equation.  Also affects the rate.
        
    Returns
    -------
    list(float)
        A list of floats that represent the change in the flowrates of the 
        different species per volume in the form:
            [dF_A/dV, dF_B/dV, dF_C/dV]
    """

    #Unpacking the flowrates at the current volume
    F_A, F_B, F_R = F
    #Concentration of A
    c_A = F_A/volumetric_flowrate 
    #Concentration of B
    c_B = F_B/volumetric_flowrate 
    #Concentration of R
    c_R = F_R/volumetric_flowrate 

    #Rate at this particular point in the volume
    r = k_f*c_A*c_B**2 - k_r*c_R**n

    #List of differentials to be returned
    dFdV = [-r, -2*r, n*r]
    return dFdV

#Programming of the ODEsolver function
# Function definition replicating ode15s
ode15s = integrator.ode(deriv)
ode15s.set_integrator('vode', method='bdf', order=15, nsteps=1e8)

#Function to house the use of the ODE solver
# Generates the final conversions per iteration using different coefficients of 
#   R
def iterative(n):
    """Function to act in iteration for each volumetric_flowrate

    Parameters
    ----------
    n : float
        The coefficient of R in the chemical equation.  This also affects the rate law

    Returns
    -------
    list
        List of values that house the initial conditions that were fed into the 
        ODE Solver, followed by the resulting values that were calculated by 
        the ODE Solver
    """
    F_0 = [volumetric_flowrate*c_A0, volumetric_flowrate*c_B0, 0]
    ode15s.set_initial_value(F_0, Volume_0)
    ode15s.set_f_params(n)
    #Only returns the last iteration of ode15s
    sol = ode15s.integrate(Volume_total)
    array = [F_0, [sol[0], sol[1], sol[2]]]
    return array

#Volumetric flow vector
coefficient_span = np.linspace(coefficient_start, coefficient_end, num) 

#Conversion vector
x = [None] * num

#For loop for iterative function
for i in range(num):
    #Feed in the current volumetric flowrate
    iter = iterative(coefficient_span[i])
    #Extract the conversion
    x[i] = (iter[0][1] - iter[1][1])/iter[0][1]

## Graphing stuff
#Conversion as a function of spacetime
plt.plot(coefficient_span, x, 'b', label='Conversion')    
plt.legend(loc='best')
plt.xlabel('Coefficient of R')
plt.ylim(0, 1)
plt.ylabel('Conversion')
plt.title('PFR-Epsilon')
plt.grid()
plt.show()