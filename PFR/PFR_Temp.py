#Script for handling PFR Conversion v. Temperature
# Still behaves isothermally, so the temperature being used during one        
# iteration will remain constant throughout the process

#Example from HW4Q1
# Elementary Liquid Phase Reaction
# A + 2B <-> R
# -rA = -(1/2)rB = k_f*cA*cB^2 - k_r*cR
# Temperature assumed to be 300 K for simplicity

#Script uses a numerical solution to the differential equations that define the 
# problem, finding the change in the flowrate per change in volume at multiple 
# points over multiple iterations.  The resulting array created from iterating 
# this process for various volumes is then plotted against the temperature that 
# was used for that specific iteration.

###Importing different libraries
# Library for solving ODEs
import scipy.integrate as integrator
# Library for plotting functions and (in our case) points
import matplotlib.pyplot as plt
# Library for number-related functions and constants
import numpy as np
# Library for math function
import math



###Variable inputs for the user to alter
#Forward activation energy - J/mol
Ea_f = 10000
#Reverse activation energy - J/mol
Ea_r = 25000
#Temperature for original k values - K
T0 = 300
#Rate constants at T0 K
# Forward reaction rate constant - L^2/(mol^2.min)
k_f0 = 12.5
# Reverse reaction rate constant - L/(mol.min)
k_r0 = 1.5

#Initial temperature to examine - K
Tstart = 100
#End temperature to examine - K
Tend = 1000

#Initial concentrations - mol/L
c_A0 = 2.8
c_B0 = 1.6

#Initial volumetric flowrate - L/min
volumetric_flowrate = 100

#Volume parameter - L
Volume_total = 6



###Other numerical values
#Gas Constant - J/(mol.K)
R = 8.314
#Dummy variable to hold 0 (the lower bound of integration) - L
Volume_0 = 0
#Number of elements to plot
num = 1000

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

#Function to get the value of k_r at T Kelvin
def k_r_fun(T=T0):
    """Function to calculate the reverse k value at a given temperature using 
    the Arrhenius Law

    Parameters
    ----------
    T : float = T0
        The temperature to find k_r for.  The default temperature is whatever 
        is given by the user

    Returns
    -------
    float 
        The value of k_r at temperature T
    """
    k_r = k_r0 * math.exp((Ea_r/R)*((1/T0) - (1/T)))
    return k_r

#ODE function for changing flow rates
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
            [dF_A/dV, dF_B/dV, dF_C/dV]
    """

    #Unpacking the rate constants
    k_f, k_r = k
    #Unpacking the flowrates
    F_A, F_B, F_R = F
    #Concentration of A
    c_A = F_A/volumetric_flowrate 
    #Concentration of B
    c_B = F_B/volumetric_flowrate 
    #COncentration of R
    c_R = F_R/volumetric_flowrate 

    #Rate at this particular point in the volume
    r = k_f*c_A*c_B**2 - k_r*c_R

    #List of differentials to be returned
    dFdV = [-r, -2*r, r]
    return dFdV

#Programming of the ODEsolver function
# Function definition replicating ode15s
ode15s = integrator.ode(deriv)
ode15s.set_integrator('vode', method='bdf', order=15, nsteps=1e8)

#Function to house the use of the ODE solver
# Generates the final conversions per iteration using different temperatures
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
    #Finding the forward k value
    k_f = k_f_fun(T)
    #Finding the reverse k value
    k_r = k_r_fun(T)
    #The initial conditons to be fed into the ODE Solver
    F_0 = [volumetric_flowrate*c_A0, volumetric_flowrate*c_B0, 0]
    #Setting the initial conditions for the ODE Solver
    ode15s.set_initial_value(F_0, Volume_0)
    #Setting up the parameters to be fed into the ODE Solver
    ode15s.set_f_params([k_f, k_r])
    #Only returns the last iteration of ode15s
    sol = ode15s.integrate(Volume_total)
    array = [F_0, [sol[0], sol[1], sol[2]]]
    return array

#Temperature vector
#   Spans from the start temperature specified to the end temperature 
#   specified, separated by the number of points specified (1000)
T_span = np.linspace(Tstart, Tend, num) 

#Conversion vector
x = [None] * num

#For loop for iterative function
for i in range(num):
    #Feed in the current temperature to be evaluated
    iter = iterative(T_span[i])
    #Extract the conversion from the end
    x[i] = (iter[0][1] - iter[1][1])/iter[0][1]

### Graphing stuff
#Conversion as a function of spacetime
plt.plot(T_span, x, 'b', label='Conversion')    
plt.legend(loc='best')
plt.xlim(Tstart, Tend)
plt.xlabel('Temperature (K)')
plt.ylim(0, 1)
plt.ylabel('Conversion')
plt.title('PFR-Temperature')
plt.grid()
plt.show()