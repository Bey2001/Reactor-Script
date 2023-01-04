# Script for handling PFR Conversion v. Temperature for an Adiabatic Reactor
#   Takes in:
#       - Lower Temperature Bound
#       - Upper Temperature Bound
#       - Heat of Formation of A
#       - Heat of Formation of B
#       - Heat of Formation of C
#       - Specific Heat of A
#       - Specific Heat of B
#       - Specific Heat of C
#   All other variables are assumed constant
#   Activation energies assumed to be for simplicity's sake

# Example from HW8Q5A
#    Elementary Liquid Phase Reaction (300 K)
#    A + B -> C
#    rate = 0.01*cA*cB

# Importing different libraries
# Library for solving ODEs
import scipy.integrate as integrator
# Library for plotting functions and (in our case) points
import matplotlib.pyplot as plt
# Library for math function
import math


# Variable inputs for the user to alter
# Initial Temperature - K
Tstart = 300
# Final temperature - K
Tend = 500
# Constants for A
#   Heat of formation of A - (cal/mol)
delta_H_A = -12000
#   Specfic heat of A - (cal/mol)
cp_A = 10
# Constants for B
#   Heat of formation of B - (cal/mol)
delta_H_B = -12000
#   Specific heat of B - (cal/mol)
cp_B = 10
# Constants for C
#   Heat of formation of C - (cal/mol)
delta_H_C = -26000


# Permanent Constants
# Forward Activation Energy - cal/mol
Ea_f = 10000
# Temperature for original k values - K
T0 = 300
# Rate Constant at T0 K - (m^3/mol.s)
k_f0 = 0.00001  # 0.01 L/mol.s
# Total Concentration - (mol/m^3)
c_T0 = 100  # 0.1 M
# Volume of the reactor - m^3
Volume = 0.350  # 350 L
# Initial Volumetric Flowrate - (m^3/s)
volumetric_flowrate = 0.002  # 2 L/s
# Gas Constant - cal/(mol.K)
R = 1.9872
# Number of elements to plot
num = 101


# Values that are calculated from parameters
# Total heat of reaction - Must be greater than 0
delta_H_r = delta_H_C - delta_H_A - delta_H_B
# Initial Concentrations
c_A0 = 0.5 * c_T0
c_B0 = 0.5 * c_T0
# Initial molar flowrates - mol/min
#   Molar flowrate of A
F_A0 = volumetric_flowrate*c_A0
#   Molar flowrate of B
F_B0 = volumetric_flowrate*c_B0
# Summing all the values of FiCpi for adiabatic calculations
sum_flow_times_cp = F_A0*cp_A + F_B0*cp_B


# Mass Balance Vectors
x_MB = [0.08045967230923323, 0.11368444243627998, 0.15600935689218873,
        0.20771623718161963, 0.2681196117262344, 0.3354575723638639,
        0.4070564068456185, 0.4797568623730684, 0.550449734538522,
        0.6165835240248068, 0.6764140097677648, 0.7290630758164341,
        0.7743775246592527, 0.8127238972063486, 0.8447711283642184,
        0.8713220272686043, 0.8931955805796422, 0.9111582581661439,
        0.9258902079303606, 0.9379743488367766, 0.9478991053019636,
        0.9560671513644587, 0.9628073857574667, 0.9683865681482834,
        0.9730203118843082, 0.9768825690707172, 0.9801136741804058,
        0.9828268848924269, 0.9851137848486439, 0.9870485593926572,
        0.9886914881404599, 0.9900916870067213, 0.9912892737358192,
        0.9923171324379488, 0.9932023302656353, 0.9939671943622123,
        0.9946302123305929, 0.9952067425388198, 0.9957095925832111,
        0.9961494766002983, 0.9965353763792126, 0.9968748539393948,
        0.9971743015432607, 0.9974391260944999, 0.9976739214507543,
        0.9978826047294184, 0.9980685178626433, 0.9982345274530088,
        0.9983830963871354, 0.9985163437110492, 0.9986360994966951,
        0.9987439510645615, 0.9988412729587093, 0.9989292619355711,
        0.9990089608615016, 0.9990812816971187, 0.9991470224041866,
        0.9992068835111425, 0.9992614823906162, 0.9993113614747238,
        0.9993570001681219, 0.9993988223166661, 0.9994372041958446,
        0.999472480083689, 0.9995049464436503, 0.9995348679981927,
        0.9995624809543933, 0.9995879963721499, 0.9996116036899696,
        0.9996334723555409, 0.9996537547106384, 0.9996725875936605,
        0.9996900949271654, 0.9997063880070701, 0.999721567426173,
        0.99973572446564, 0.9997489413339075, 0.9997612932741657,
        0.9997728478773129, 0.9997836672924498, 0.999793807656993,
        0.999803320590541, 0.9998122524893311, 0.9998206464572896,
        0.9998285416241495, 0.9998359739541977, 0.9998429760489136,
        0.9998495783184937, 0.9998558083328757, 0.9998616916931382,
        0.999867251755885, 0.9998725101790337, 0.999877487018482,
        0.9998822004393851, 0.9998866676516436, 0.9998909042848342,
        0.999894924931038, 0.9998987430545454, 0.9999023711544766,
        0.9999058208379039, 0.9999091028756951]

T_MB = [300,  307,  314,  321,  328,  335,  342,  349,  356,  363,  370,  377,
        384,  391,  398,  405,  412,  419,  426,  433,  440,  447,  454,  461,
        468,  475,  482,  489,  496,  503,  510,  517,  524,  531,  538,  545,
        552,  559,  566,  573,  580,  587,  594,  601,  608,  615,  622,  629,
        636,  643,  650,  657,  664,  671,  678,  685,  692,  699,  706,  713,
        720,  727,  734,  741,  748,  755,  762,  769,  776,  783,  790,  797,
        804,  811,  818,  825,  832,  839,  846,  853,  860,  867,  874,  881,
        888,  895,  902,  909,  916,  923,  930,  937,  944,  951,  958,  965,
        972,  979,  986,  993, 1000, ]

# ODE function for changing flow rates


def EnergyBalance(Volume, F):
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
            [dF_A/dV, dF_B/dV, dT/dV, dv]
    """

    # Unpacking the next iteration of values
    F_A, F_B, T, v = F
    # Concentration of A
    c_A = F_A/v
    # Concentration of B
    c_B = F_B/v

    # Getting the forward reaction rate constant
    k_f = k_f0 * math.exp((Ea_f/R)*((1/T0) - (1/T)))

    # Rate at this particular point in the volume
    r = k_f*c_A*c_B

    # List of differentials to be returned
    dFdV = [-r, -r, -r*delta_H_r/sum_flow_times_cp, 0]
    return dFdV


# Vector spanning from 0 to the volume given
volume_span = [0, Volume]
# The initial conditions to be fed into the ODE Solver
initial_conditions = [F_A0, F_B0, T0, volumetric_flowrate]

# Using integrate.solve_ivp to solve the energy balance equations
solution = integrator.solve_ivp(
    EnergyBalance, volume_span, initial_conditions, method='BDF')

# Pulling out the flowrate of B
F_A0_arr = solution.y[0]
# Pulling out the temperature vector
T_EB = solution.y[2]

# Calculating the conversion vector
x_EB = 1 - F_A0_arr/F_A0_arr[0]

# Graphing stuff
# Conversion as a function of spacetime
plt.plot(T_MB, x_MB, 'b', label='Mass Balance')
plt.plot(T_EB, x_EB, 'r', label='Energy Balance')
plt.legend(loc='best')
plt.xlim(Tstart, Tend)
plt.xlabel('Temperature (K)')
plt.ylim(0, 1)
plt.ylabel('Conversion')
plt.title('PFR-Adiabatic')
plt.grid()
plt.show()
