#Script for handling PFR Conversion v. Temperature while adiabatic
#   Will graph both the Material Balance and Energy Balance

#Example from HW4Q1
# Elementary Liquid Phase Reaction
# A + 2B <-> R
# -rA = -(1/2)rB = k_f*cA*cB^2 - k_r*cR

#Script uses a different numerical approach to finding the conversion of 
# product as a function of T using an energy balance.  This requires an ODE 
# Solver function since the PFR must still be integrated, rather than making a 
# simple linear equation like a CSTR does.  This can be seen in the different 
# volume found from PFR_Temp.py

#Future improvements for this script could include attaching the code or in 
# some way executing PFR_Temp.py to print the Mass Balance produced there onto 
# the same graph as the Energy Balance produced here

###Importing different libraries
# Library for solving ODEs
import scipy.integrate as integrator
# Library for plotting functions and (in our case) points
import matplotlib.pyplot as plt
# Library for math function
import math



###Variable inputs for the user to alter
#Constants for A
#   Heat of formation of A
delta_H_A = -40000
#   Specfic heat of A
cp_A = 5
#Constants for B
#   Heat of formation of B
delta_H_B = -30000
#   Specific heat of B
cp_B = 10
#Constants for C
#   Heat of formation of C
delta_H_R = -45000
#   Specific heat of C
cp_R = 5

#Forward Activation Energy - J/mol
Ea_f = 70000
#Reverse Activation Energy - J/mol
Ea_r = 25000
#Temperature for original k values
T0 = 300
#Rate Constants at T0 K
# Forward reaction rate constant - L^2/(mol^2.min)
k_f0 = 12.5
# Reverse reaction rate constant - L/(mol.min)
k_r0 = 1.5

#Heat Coefficient - W/m^2K
U = 630
#Area for heat transfer - m^2
A = 1
#Surface Temperature of the heat exchanger - K
T_A = 250

#Initial Temperature - K
Tstart = 300

#Initial Concentrations - mol/L
c_A0 = 2.8
c_B0 = 1.6
c_R0 = 0

#Initial Volumetric Flowrate - L/min
volumetric_flowrate = 100

#Volume parameter - L
Volume_total = 6



###Other numerical values
#Number of elements to plot
num = 1000
#Volume parameters
Volume_0 = 0
# Gas Constant - J/(mol.K)
R = 8.314



###Values that are calculated from parameters
#Total heat of reaction
delta_H_r = delta_H_R - delta_H_A - 2*delta_H_B
#Initial molar flowrates
# Molar flowrate of A
F_A0 = volumetric_flowrate*c_A0
# Molar flowrate of B
F_B0 = volumetric_flowrate*c_B0
# Molar flowrate of R
F_R0 = volumetric_flowrate*c_R0
#Summing all the values of FiCpi for adiabatic calculations
sum_flow_times_cp = F_A0*cp_A + F_B0*cp_B + F_R0*cp_R



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

#ODE Function for changing flow rates
def EnergyBalance(V, F):
    """Function to be used in an odesolver
    
    Parameters
    ----------
    Volume : float
        Value used by the odesolver.  Akin to "t" in normal context and usage.
        Represents the slice of volume of the PFR 
    F : (float, float, float, float, float)
        Tuple of three objects representing the current values of:
        (the flowrate of A, the flowrate of B, the flowrate of R, Temperature, 
        volumetric flowrate)
        
    Returns
    -------
    list(float)
        A list of floats that represent the change in the flowrates of the 
        different species per volume in the form:
            [dF_A/dV, dF_B/dV, dF_C/dV, dT/dV, dv]
    """

    #Unpacking the next iteration of values
    F_A, F_B, F_R, T, v = F
    #Concentration of A
    c_A = F_A/v 
    #Concentration of B
    c_B = F_B/v 
    #Concentration of R
    c_R = F_R/v 

    #Getting the forward reaction rate constant
    k_f = k_f_fun(T)
    #Getting the reverse reaction rate constant
    k_r = k_r_fun(T)

    #Rate at this particular point in the volume
    r = k_f*c_A*c_B**2 - k_r*c_R

    #List of differentials to be returned
    dFdV = [-r, -2*r, r, -(r*delta_H_r + U*A*(T - T_A))/sum_flow_times_cp, v - volumetric_flowrate*T/T0]
    return dFdV

#Vector spanning from 0 to the volume given
volume_span = [Volume_0, Volume_total]
#The initial conditions to be fed into the ODE Solver
initial_conditions = [F_A0, F_B0, F_R0, Tstart, volumetric_flowrate]

#Using integrate.solve_ivp to solve the energy balance equations
solution = integrator.solve_ivp(EnergyBalance, volume_span, initial_conditions, method='BDF')

#Pulling out the flowrate of B
F_B0_arr = solution.y[1]
#Pulling out the temperature vector
T_arr = solution.y[3]

#Calculating the conversion vector
conversion = 1 - F_B0_arr/F_B0_arr[0]

## Graphing stuff
#Conversion as a function of spacetime
plt.plot(T_arr, conversion, 'b', label='Conversion')    
plt.legend(loc='best')
plt.xlabel('Temperature (K)')
plt.ylim(0, 1)
plt.ylabel('Conversion')
plt.grid()
plt.show()