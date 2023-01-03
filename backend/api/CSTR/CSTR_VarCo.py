#Script for handling CSTR Conversion v. Spacetime
#   All other variables are assumed constant
#   Activation energies assumed to be for simplicity's sake

#Example from HW8Q5
# Elementary Liquid Phase Reaction (300 K)
# A + nB -> C
# rate = 0.01*cA*cB

#Script uses an algebraic solver function.  This does lead to issues with some 
# values since the solver itself does not have limitations/constraints on its 
# calculations, thus multiple or inaccurate solutions can be reported in the 
# graph, leading to some shapes that should not exist and disrupting curves.

###Importing different libraries
# Library for finding 0s to algebraic equations
from scipy.optimize import fsolve
# Library for plotting functions and (in our case) points
import matplotlib.pyplot as plt
# Library for number-related functions and constants
import numpy as np



###Variable inputs for the user to alter
# Coefficient to investigate
n = 1



### Permanent Constants
# Rate Constant at 300 K - (m^3/mol.s)
k = 0.00001
#Total Concentration - (kmol/m^3)
c_T0 = 100
#Volume of the reactor - m^3
volume = 0.350
#Lower Volumetric Flowrate - m^3/s
lower_flowrate = 0.00001
# Upper Volumetric Flowrate - m^3/s
upper_flowrate = 10
#Number of elements to plot
num = 100



###Values that are calculated from parameters
#Calculation of initial concentrations
c_A0 = 0.5 * c_T0
spacetime_start = volume / upper_flowrate
spacetime_end = volume / lower_flowrate
spacetime_span = np.linspace(spacetime_start, spacetime_end, num)



# Basis Vectors
# spacetime_basis = [0.035, 350.03465, 700.0343, 1050.03395, 1400.0336, 1750.03325, 2100.0329, 2450.03255, 2800.0322, 3150.03185,
# 3500.0315, 3850.03115, 4200.0308, 4550.03045, 4900.0301, 5250.02975, 5600.0294, 5950.02905, 6300.0287, 6650.02835,
# 7000.028, 7350.02765, 7700.0273, 8050.02695, 8400.0266, 8750.02625, 9100.0259, 9450.02555, 9800.0252, 10150.02485,
# 10500.0245, 10850.02415, 11200.0238, 11550.02345, 11900.0231, 12250.02275, 12600.0224, 12950.02205, 13300.0217, 13650.02135,
# 14000.021, 14350.02065, 14700.0203, 15050.01995, 15400.0196, 15750.01925, 16100.0189, 16450.01855, 16800.0182, 17150.01785,
# 17500.0175, 17850.01715, 18200.0168, 18550.01645, 18900.0161, 19250.01575, 19600.0154, 19950.01505, 20300.0147, 20650.01435,
# 21000.014, 21350.01365, 21700.0133, 22050.01295, 22400.0126, 22750.01225, 23100.0119, 23450.01155, 23800.0112, 24150.01085,
# 24500.0105, 24850.01015, 25200.0098, 25550.00945, 25900.0091, 26250.00875, 26600.0084, 26950.00805, 27300.0077, 27650.00735,
# 28000.007, 28350.00665, 28700.0063, 29050.00595, 29400.0056, 29750.00525, 30100.0049, 30450.00455, 30800.0042, 31150.00385,
# 31500.0035, 31850.00315, 32200.0028, 32550.00245, 32900.0021, 33250.00175, 33600.0014, 33950.00105, 34300.0007, 34650.00035,
# 35000.0]

# conversion_basis = [2e-05, 0.13189, 0.21544, 0.27555, 0.32189, 0.35925, 0.39031, 0.41674, 0.43963, 0.45973,
# 0.47759, 0.49362, 0.50811, 0.52131, 0.5334, 0.54454, 0.55485, 0.56443, 0.57336, 0.58172,
# 0.58957, 0.59696, 0.60394, 0.61053, 0.61679, 0.62272, 0.62838, 0.63376, 0.63891, 0.64382,
# 0.64853, 0.65305, 0.65738, 0.66154, 0.66555, 0.66941, 0.67313, 0.67672, 0.68018, 0.68353,
# 0.68677, 0.68991, 0.69295, 0.6959, 0.69876, 0.70153, 0.70423, 0.70685, 0.70939, 0.71187,
# 0.71429, 0.71664, 0.71893, 0.72116, 0.72334, 0.72546, 0.72753, 0.72956, 0.73154, 0.73347,
# 0.73536, 0.73721, 0.73902, 0.74079, 0.74252, 0.74422, 0.74588, 0.74751, 0.7491, 0.75067,
# 0.7522, 0.75371, 0.75518, 0.75663, 0.75806, 0.75945, 0.76082, 0.76217, 0.7635, 0.7648,
# 0.76608, 0.76734, 0.76857, 0.76979, 0.77098, 0.77216, 0.77332, 0.77446, 0.77558, 0.77669,
# 0.77778, 0.77885, 0.77991, 0.78095, 0.78197, 0.78298, 0.78398, 0.78496, 0.78593, 0.78688,
# 0.78782]


# # Basis Vector
# conversion_basis = [None] * num
# basis_eqn = lambda x, st: k * st * c_A0 - x / ((1 - x) ** 2)


# if (n > 1):
#     # k.tau = (1/c_A0^n).(x_A/(1 - x_A)).(1/(1-n.x_A)^n))
#     base_eqn = lambda x, st: k * st * (c_A0 ** n) - x / ((1 - x) * ((1 - n * x) ** n))    
# elif (n == 1):
#     # k.tau = x_A/(c_A0.(1-x_A)^2)
#     base_eqn = basis_eqn
# else:
#     # k.tau.c_A0^n = (x_A/(1 - x_A)).(1/(1-n.x_A)^n))
#     base_eqn = lambda x, st: k * st * (c_A0 ** n) - x / ((1 - x) * ((1 - n * x) ** n))

# Basis Vector
conversion_basis = [None] * num
basis_eqn = lambda x, st: k * st - x / (1 - x)

   
if (n == 1):
    # k.tau = x_A/(c_A0.(1-x_A)^2)
    base_eqn = basis_eqn
else:
    # k.tau.c_A0^n = (x_A/(1 - x_A)).(1/(1-n.x_A)^n))
    base_eqn = lambda x, st: k * st * (c_A0 ** (n - 1)) - x / ((1 - x) ** n)

#Conversion vector
x = [None] * num

#For loop for iterative function
for i in range(num):
    spacetime = spacetime_span[i]
    #Algebraic equation
    eqn = lambda x : base_eqn(x, spacetime)
    #Initial Guess for fsolve
    initial_guess = 0.99
    #Extract the conversion
    x[i] = fsolve(eqn, initial_guess, xtol=1e-10)[0]
    if n == 1:
        conversion_basis[i] = x[i]
    else:
        basis_equation = lambda x: basis_eqn(x, spacetime)
        conversion_basis[i] = fsolve(basis_equation, initial_guess)[0]

### Graphing stuff
plt.plot(spacetime_span, conversion_basis, 'b', label='Coefficient of A = 1')
label = 'Coefficient of A = {}'.format('{:f}'.format(n).rstrip('.0'))
plt.plot(spacetime_span, x, 'r', label=label)    
plt.legend(loc='best')
plt.xlim(spacetime_start, spacetime_end)
plt.xlabel('Spacetime')
plt.ylim(0, 1)
plt.ylabel('Conversion of A')
plt.grid()
plt.show()