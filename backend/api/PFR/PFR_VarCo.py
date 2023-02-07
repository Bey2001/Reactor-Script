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
n = 3


# Permanent Constants
# Rate Constant at 300 K - (m^3/mol.s)
k = 0.00001
# Total Concentration - (kmol/m^3)
c_T0 = 100
# Volume of the reactor - m^3
volume = 0.350
# Lower Volumetric Flowrate - m^3/s
v_0 = 0.00001
# Number of elements to plot
num = 100


# Values that are calculated from parameters
# Calculation of initial concentrations
c_A0 = 0.5 * c_T0
c_B0 = 0.5 * c_T0
c_C0 = 0
F_A0 = c_A0 * v_0
F_B0 = c_B0 * v_0
F_C0 = c_C0 * v_0
F_T0 = F_A0 + F_B0 + F_C0

initial_conditions = [F_A0, F_B0, F_C0]

conversion_basis = [0.0, 0.1601764918147195, 0.29281267508514985, 0.4013934247083134, 0.4898800369150772, 0.5623928460854468, 0.6213454631183273, 0.6691514989126237, 0.7082245643672409, 0.7406120271404572, 0.7678656354590265, 0.790839307676598, 0.8102109495234008, 0.8266584667296639, 0.8408178801263928, 0.8530840338459089, 0.863876698742834, 0.8733637069555324, 0.8817128906223685, 0.8890920818817065, 0.895669112871911, 0.9015614992871734, 0.9068900401998041, 0.911742495901042, 0.9161600724693791, 0.920183975983308, 0.923855412521321, 0.9272155881619103, 0.9303057089835682, 0.9331669810647872, 0.9358003995739377, 0.9382349414086054, 0.9405179694584148, 0.94265785811776, 0.9446629817810352, 0.9465417148426348, 0.9483024316969527, 0.9499535067383833, 0.9515033143613207, 0.9529602289601592, 0.9543326249292928, 0.9556288766631158, 0.9568573585560225, 0.958026445002407, 0.9591445103966634, 0.9601835508187004, 0.961172446193365, 0.9621210568578217, 0.9630307575053061, 0.9639029228290535,
                    0.9647389275222997, 0.9655401462782799, 0.9663079537902297, 0.9670437247513846, 0.9677488338549799, 0.9684246557942514, 0.9690725652624343, 0.9696939369527643, 0.9702901455584768, 0.9708625657728073, 0.9714125722889911, 0.971941539800264, 0.9724508429998613, 0.9729418565810185, 0.9734159552369711, 0.9738745136609546, 0.9743189065462045, 0.9747505085859562, 0.9751634983405524, 0.9755637117679327, 0.9759528931914234, 0.9763313150212133, 0.9766992496674914, 0.9770569695404467, 0.977404747050268, 0.9777428546071443, 0.9780715646212643, 0.9783911495028174, 0.978701881661992, 0.9790040335089775, 0.9792978774539625, 0.979583685907136, 0.9798617312786869, 0.9801322859788043, 0.980395622417677, 0.9806520130054939, 0.9809017301524439, 0.981145046268716, 0.9813822337644992, 0.9816135650499822, 0.9818393125353542, 0.9820597486308039, 0.9822751457465204, 0.9824857762926925, 0.9826919126795093, 0.9828938273171595, 0.9830917926158321, 0.983286080985716, 0.9834769648370003, 0.9836647165798738, 0.9838496086245254]

# ODE function for changing flow rates


def dFdV(Volume, F):

    # Unpacking the flowrates at the current volume
    F_A, F_B, F_C = F
    F_T = F_A + F_B + F_C

    volumetric_flowrate = v_0 * (F_T / F_T0)
    # Concentration of A
    c_A = F_A / volumetric_flowrate
    # Concentration of B
    c_B = F_B / volumetric_flowrate

    # Rate at this particular point in the volume
    r = k * c_A * c_B

    # List of differentials to be returned
    dFdV = [-r, -r, n * r]
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
plt.plot(spacetime, conversion_basis, 'b', label='Coefficient of C = 1')
label = 'Coefficient of C = {}'.format('{:f}'.format(n).rstrip('.0'))
plt.plot(spacetime, conversion, 'r', label=label)
plt.legend(loc='best')
plt.xlim(spacetime[0], spacetime[-1])
plt.xlabel('Spacetime (s)')
plt.ylim(0, 1)
plt.ylabel('Conversion of A')
plt.grid()
plt.show()
