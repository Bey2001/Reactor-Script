# Script for handling CSTR Conversion v. Spacetime
#   All other variables are assumed constant
#   Activation energies assumed to be for simplicity's sake

# Example from HW8Q5
# Elementary Liquid Phase Reaction (300 K)
# A + nB -> C
# rate = 0.01*cA*cB

# Script uses a numerical solution to the differential equations that define the
# problem, finding the change in the flowrate per change in volume at multiple
# points over multiple iterations.  The resulting array created from iterating
# this process for various volumes is then plotted against the coefficient of R
# that was used for that specific iteration.

# Importing different libraries
# Library for solving ODEs
import scipy.integrate as integrator
# Library for plotting functions and (in our case) points
import matplotlib.pyplot as plt
# Library for number-related functions and constants
import numpy as np


# Variable inputs for the user to alter
# Coefficient to investigate
n = 3.5


# Permanent Constants
# Rate Constant at 300 K - (m^3/mol.s)
k = 0.00001
# Total Concentration - (kmol/m^3)
c_T0 = 100
# Volume of the reactor - m^3
volume = 0.350
# Lower Volumetric Flowrate - m^3/s
lower_flowrate = 0.00001
# Upper Volumetric Flowrate - m^3/s
upper_flowrate = 10
# Number of elements to plot
num = 100


# Values that are calculated from parameters
# Calculation of initial concentrations
c_A0 = 0.5 * c_T0
c_B0 = 0.5 * c_T0
spacetime_start = volume / upper_flowrate
spacetime_end = volume / lower_flowrate
spacetime_span = np.linspace(spacetime_start, spacetime_end, num)

conversion_basis = [
    1.7499241517157317e-05, 0.1502267981133905, 0.2612058884719971, 0.3465455301501841, 0.414210688277733, 0.4691771009245152, 0.5147139042461059, 0.5530550357402704, 0.585780171407869, 0.6140403764163188, 0.6386899022306443, 0.6603805979249234, 0.6796145133795515, 0.6967865155275922, 0.712211487774843, 0.7261428890498782, 0.7387875052979261, 0.7503159159810814, 0.7608699794013326, 0.7705681181156898, 0.779510238350729, 0.7877814492482593, 0.7954545815289086, 0.8025922299958015, 0.8092485262071847, 0.8154705765751966, 0.8212995482383247, 0.8267715490946894, 0.8319183912533238, 0.8367682184343626, 0.8413460222877002, 0.8456740660078944, 0.8497722318383304, 0.8536583537495859, 0.8573484837514791, 0.8608570901311107, 0.864197250844646, 0.8673808241497564, 0.8704185561474554, 0.8733202426291657, 0.8760948177499593, 0.8787504587736301, 0.8812946552438842, 0.8837342779536708, 0.8860756437885755, 0.8883245709956753, 0.890486427703738, 0.8925661739468943, 0.8945684003756833, 0.8964973619247629, 0.8983570087084405, 0.9001510092993144, 0.901882774429094, 0.9035554907990088, 0.9051721194251173, 0.9067354494219388, 0.9082480612281765, 0.909712400711437, 0.9111307311708882, 0.9125051970945526, 0.9138377944356145, 0.9151304101660706, 0.9163848139301336, 0.9176026780853579, 0.9187855723117252, 0.9199349856646863, 0.9210523164102522, 0.92213889319028, 0.9231959656997392, 0.9242247220514175, 0.9252262829055174, 0.9262017140050581, 0.9271520231071709, 0.9280781696130093, 0.9289810620757131, 0.9298615668083108, 0.9307205050188039, 0.9315586607799408, 0.9323767782621104, 0.9331755685835744, 0.9339557077538695, 0.9347178419047603, 0.9354625849499286, 0.9361905266001553, 0.9369022305772017, 0.9375982283522132, 0.9382790388291344, 0.9389451580456484, 0.939597046791151, 0.9402351627344165, 0.9408599418908397, 0.9414717904555135, 0.9420711096774365, 0.942658282461978, 0.943233671071089, 0.9437976271632356, 0.9443504888388962, 0.9448925792185238, 0.9454242099861352, 0.9459456819633106]

# ODE function for changing flow rates


def deriv(Volume, F, flowrate):
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

    # Unpacking the flowrates at the current volume
    F_A, F_B = F
    # Concentration of A
    c_A = F_A/flowrate
    # Concentration of B
    c_B = F_B/flowrate

    # Rate at this particular point in the volume
    r = k * c_A * (c_B ** n)

    # List of differentials to be returned
    dFdV = [-r, -r]
    return dFdV


# Programming of the ODEsolver function
# Function definition replicating ode15s
ode15s = integrator.ode(deriv)
ode15s.set_integrator('vode', method='bdf', order=15, nsteps=1e8)

# Function to house the use of the ODE solver
# Generates the final conversions per iteration using different coefficients of
#   B


def iterative(spacetime):
    """Function to act in iteration for each volumetric_flowrate

    Parameters
    ----------
    n : float
        The coefficient of B in the chemical equation.  This also affects the rate law

    Returns
    -------
    list
        List of values that house the initial conditions that were fed into the 
        ODE Solver, followed by the resulting values that were calculated by 
        the ODE Solver
    """
    flowrate = volume / spacetime

    F_0 = [flowrate*c_A0, flowrate * c_B0]
    ode15s.set_initial_value(F_0, 0)
    ode15s.set_f_params(flowrate)
    # Only returns the last iteration of ode15s
    sol = ode15s.integrate(volume)
    array = [F_0, [sol[0], sol[1]]]
    return array


# Conversion vector
x = [None] * num

# For loop for iterative function
for i in range(num):
    # Feed in the current volumetric flowrate
    iter = iterative(spacetime_span[i])
    # Extract the conversion
    x[i] = (iter[0][1] - iter[1][1])/iter[0][1]

# Graphing stuff
# Conversion as a function of spacetime
plt.plot(spacetime_span, conversion_basis, 'b', label='Coefficient of B = 1')
label = 'Coefficient of B = {}'.format('{:f}'.format(n).rstrip('.0'))
plt.plot(spacetime_span, x, 'r', label=label)
plt.legend(loc='best')
plt.xlim(spacetime_start, spacetime_end)
plt.xlabel('Spacetime (s)')
plt.ylim(0, 1)
plt.ylabel('Conversion')
plt.title('PFR-Epsilon')
plt.grid()
plt.show()

conversion_basis.reverse()
print(conversion_basis)
