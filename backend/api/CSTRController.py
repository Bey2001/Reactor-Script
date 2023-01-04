from flask import send_file
from flask_restful import Resource, reqparse
import matplotlib.pyplot as plt
import numpy as np
import io
# Function for finding 0s to algebraic equations
from scipy.optimize import fsolve
import math


class CSTREnergyBalanceApiHandler(Resource):
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

    # Mass Balance vectors - Length 101 to have clean numbers
    # These are actually constant, regardless of values input by user
    #   Conversion vector for the mass balance
    #   - Constant across the temperature, regardless of thermodynamic properties
    #   - Calculated by using the original CSTR_Adiabatic script from 300 to 1000K
    x_MB = [0.075, 0.103, 0.138, 0.177, 0.222, 0.269, 0.319, 0.368, 0.417, 0.463,
            0.507, 0.549, 0.587, 0.622, 0.653, 0.683, 0.709, 0.733, 0.754, 0.774,
            0.791, 0.807, 0.822, 0.835, 0.847, 0.858, 0.867, 0.876, 0.884, 0.892,
            0.899, 0.905, 0.911, 0.916, 0.921, 0.925, 0.929, 0.933, 0.936, 0.94,
            0.943, 0.946, 0.948, 0.951, 0.953, 0.955, 0.957, 0.959, 0.961, 0.962,
            0.964, 0.965, 0.967, 0.968, 0.969, 0.97, 0.971, 0.972, 0.973, 0.974,
            0.975, 0.976, 0.977, 0.977, 0.978, 0.979, 0.979, 0.98, 0.98, 0.981,
            0.982, 0.982, 0.983, 0.983, 0.983, 0.984, 0.984, 0.985, 0.985, 0.985,
            0.986, 0.986, 0.986, 0.987, 0.987, 0.987, 0.988, 0.988, 0.988, 0.988,
            0.989, 0.989, 0.989, 0.989, 0.989, 0.99, 0.99, 0.99, 0.99, 0.99,
            0.991]
    #   Temperature vector for the mass balance
    T_MB = [300.0, 307.0, 314.0, 321.0, 328.0, 335.0, 342.0, 349.0, 356.0, 363.0,
            370.0, 377.0, 384.0, 391.0, 398.0, 405.0, 412.0, 419.0, 426.0, 433.0,
            440.0, 447.0, 454.0, 461.0, 468.0, 475.0, 482.0, 489.0, 496.0, 503.0,
            510.0, 517.0, 524.0, 531.0, 538.0, 545.0, 552.0, 559.0, 566.0, 573.0,
            580.0, 587.0, 594.0, 601.0, 608.0, 615.0, 622.0, 629.0, 636.0, 643.0,
            650.0, 657.0, 664.0, 671.0, 678.0, 685.0, 692.0, 699.0, 706.0, 713.0,
            720.0, 727.0, 734.0, 741.0, 748.0, 755.0, 762.0, 769.0, 776.0, 783.0,
            790.0, 797.0, 804.0, 811.0, 818.0, 825.0, 832.0, 839.0, 846.0, 853.0,
            860.0, 867.0, 874.0, 881.0, 888.0, 895.0, 902.0, 909.0, 916.0, 923.0,
            930.0, 937.0, 944.0, 951.0, 958.0, 965.0, 972.0, 979.0, 986.0, 993.0,
            1000.0]


class CSTRAdiabaticApiHandler(CSTREnergyBalanceApiHandler):

    def get(self):
        parser = reqparse.RequestParser()

        # Parse the query args
        parser.add_argument('lowerTemp', type=float)
        parser.add_argument('upperTemp', type=float)
        parser.add_argument('cA', type=float)
        parser.add_argument('hfA', type=float)
        parser.add_argument('cB', type=float)
        parser.add_argument('hfB', type=float)
        parser.add_argument('hfC', type=float)

        args = parser.parse_args()

        # Variable inputs for the user to alter
        # Initial Temperature - K
        t_start = args.get('lowerTemp')
        if (t_start is None):
            return {
                "status": "Success",
                "message": "Lower temperature bound not provided"
            }
        # Final temperature - K
        t_end = args.get('upperTemp')
        if (t_end is None):
            return {
                "status": "Success",
                "message": "Upper temperature bound not provided"
            }
        # Constants for A
        #   Heat of formation of A - (cal/mol)
        delta_H_A = args.get('hfA')
        if (delta_H_A is None):
            return {
                "status": "Success",
                "message": "Heat of Formation of A not provided"
            }
        #   Specfic heat of A - (cal/mol)
        cp_A = args.get('cA')
        if (cp_A is None):
            return {
                "status": "Success",
                "message": "Specific Heat of A not provided"
            }
        # Constants for B
        #   Heat of formation of B - (cal/mol)
        delta_H_B = args.get('hfB')
        if (delta_H_B is None):
            return {
                "status": "Success",
                "message": "Heat of Formation of B not provided"
            }
        #   Specific heat of B - (cal/mol)
        cp_B = args.get('cB')
        if (cp_B is None):
            return {
                "status": "Success",
                "message": "Specific Heat of B not provided"
            }
        # Constants for C
        #   Heat of formation of C - (cal/mol)
        delta_H_C = args.get('hfC')
        if (delta_H_C is None):
            return {
                "status": "Success",
                "message": "Heat of Formation of C not provided"
            }

        plot = self.plot(t_start, t_end, delta_H_A, cp_A,
                         delta_H_B, cp_B, delta_H_C)

        # https://stackoverflow.com/questions/50728328/python-how-to-show-matplotlib-in-flask
        return send_file(plot,
                         attachment_filename='plot.png',
                         mimetype='image/png')

    def plot(self, t_start, t_end, delta_H_A, cp_A, delta_H_B, cp_B, delta_H_C):
        # Values that are calculated from parameters
        # Total heat of reaction - Must be greater than 0
        delta_H_r = delta_H_C - delta_H_A - delta_H_B
        # Summing up all the heat capacities of species in the feed
        sum_theta_cp = cp_A + cp_B

        # Energy Balance vectors
        # Simple linear calculations
        T_EB = np.linspace(t_start, t_end, self.num)
        x_EB = [(T - self.T0)*(-sum_theta_cp/delta_H_r) for T in T_EB]
        # Graphing stuff
        # Conversion as a function of spacetime
        plt.plot(self.T_MB, self.x_MB, 'b', label='Material Balance')
        plt.plot(T_EB, x_EB, 'r', label='Energy Balance')
        plt.legend(loc='best')
        plt.xlim(t_start, t_end)
        plt.xlabel('Temperature (K)')
        plt.ylim(0, 1)
        plt.ylabel('Conversion')
        plt.grid()

        bytes_image = io.BytesIO()
        plt.savefig(bytes_image, format='png')
        bytes_image.seek(0)
        plt.close()
        return bytes_image


class CSTRHeatExchangerApiHandler(CSTREnergyBalanceApiHandler):
    # Permanent Constants
    # Constants for A
    #   Heat of formation of A - (cal/mol)
    delta_H_A = -20000
    #   Specfic heat of A - (cal/mol)
    cp_A = 15
    # Constants for B
    #   Heat of formation of B - (cal/mol)
    delta_H_B = -15000
    #   Specific heat of B - (cal/mol)
    cp_B = 15
    # Constants for C
    #   Heat of formation of C - (cal/mol)
    delta_H_C = -41000
    #   Specific heat of C - (cal/mol)
    cp_C = 30

    # Values that are calculated from parameters
    # Total heat of reaction
    delta_H_r = delta_H_C - delta_H_A - delta_H_B
    # Difference in the heat capacities of the chemical species
    delta_cp = cp_C - cp_A - cp_B
    # Calculation of initial concentrations
    #   Initial concentration of A
    c_A0 = 0.5 * CSTREnergyBalanceApiHandler.c_T0
    # Initial Molar Flowrate (mol/s)
    F_A0 = CSTREnergyBalanceApiHandler.volumetric_flowrate*c_A0
    # Summing up all the heat capacities of species in the feed
    sum_theta_cp = cp_A + cp_B

    def get(self):
        parser = reqparse.RequestParser()

        # Parse the query args
        parser.add_argument('lowerTemp', type=float)
        parser.add_argument('upperTemp', type=float)
        parser.add_argument('u', type=float)
        parser.add_argument('a', type=float)
        parser.add_argument('tSurface', type=float)

        args = parser.parse_args()

        # Variable inputs for the user to alter
        # Initial Temperature - K
        t_start = args.get('lowerTemp')
        if (t_start is None):
            return {
                "status": "Success",
                "message": "Lower temperature bound not provided"
            }
        # Final temperature - K
        t_end = args.get('upperTemp')
        if (t_end is None):
            return {
                "status": "Success",
                "message": "Upper temperature bound not provided"
            }
        u = args.get('u')
        if (u is None):
            return {
                "status": "Success",
                "message": "Heat Transfer Coefficient not provided"
            }
        a = args.get('a')
        if (a is None):
            return {
                "status": "Success",
                "message": "Area of Heat Transfer not provided"
            }
        t_surface = args.get('tSurface')
        if (t_surface is None):
            return {
                "status": "Success",
                "message": "Surface Temperature of Exchange Site not provided"
            }

        plot = self.plot(t_start, t_end, u, a, t_surface)

        # https://stackoverflow.com/questions/50728328/python-how-to-show-matplotlib-in-flask
        return send_file(plot,
                         attachment_filename='plot.png',
                         mimetype='image/png')

    def plot(self, t_start, t_end, u, a, t_surface):
        # Energy Balance vectors
        # Simple linear calculations
        T_EB = np.linspace(t_start, t_end, self.num)
        x_EB = [(u*a*(t_surface - T) - self.F_A0 * self.sum_theta_cp * (T - self.T0)) /
                (self.F_A0 * (self.delta_cp * (T - self.T0) + self.delta_H_r)) for T in T_EB]

        # Graphing stuff
        # Conversion as a function of spacetime
        plt.plot(self.T_MB, self.x_MB, 'b', label='Material Balance')
        plt.plot(T_EB, x_EB, 'r', label='Energy Balance')
        plt.legend(loc='best')
        plt.xlim(t_start, t_end)
        plt.xlabel('Temperature (K)')
        plt.ylim(0, 1)
        plt.ylabel('Conversion')
        plt.grid()

        bytes_image = io.BytesIO()
        plt.savefig(bytes_image, format='png')
        bytes_image.seek(0)
        plt.close()
        return bytes_image


class CSTRSpacetimeApiHandler(Resource):
    # Permanent Constants
    # Total Concentration  - (mol/m^3)
    c_T0 = 100
    # Forward Activation Energy - cal/mol
    e_a = 10000
    # Rate Constant - (m^3/mol.s)
    k = 0.00001
    # Temperature for original k values - K
    T0 = 300
    # Gas Constant - cal/(mol.K)
    R = 1.9872
    # Number of elements to plot
    num = 101

    # Values that are calculated from constants
    # Calculation of initial concentrations
    #   Initial concentration of A
    c_A0 = 0.5 * c_T0

    def get(self):
        parser = reqparse.RequestParser()

        # Parse the query args
        parser.add_argument('lowerFlowrate', type=float)
        parser.add_argument('upperFlowrate', type=float)
        parser.add_argument('volume', type=float)

        args = parser.parse_args()

        # Variable inputs for the user to alter
        # Initial Temperature - K
        flow_start = args.get('lowerFlowrate')
        if (flow_start is None):
            return {
                "status": "Success",
                "message": "Lower temperature bound not provided"
            }
        # Final temperature - K
        flow_end = args.get('upperFlowrate')
        if (flow_end is None):
            return {
                "status": "Success",
                "message": "Upper temperature bound not provided"
            }
        volume = args.get('volume')
        if (volume is None):
            return {
                "status": "Success",
                "message": "Activation Energy not provided"
            }

        plot = self.plot(flow_start, flow_end, volume)

        # https://stackoverflow.com/questions/50728328/python-how-to-show-matplotlib-in-flask
        return send_file(plot,
                         attachment_filename='plot.png',
                         mimetype='image/png')

    def plot(self, flow_start, flow_end, volume):
        spacetime_start = volume / flow_end
        spacetime_end = volume / flow_start
        # Temperature vector
        spacetime_span = np.linspace(spacetime_start, spacetime_end, self.num)

        # Conversion vector
        x = [None] * self.num

        # For loop for iterative function
        for i in range(self.num):
            # Finding the rate constants
            spacetime = spacetime_span[i]
            # Algebraic equation
            def eqn(x): return spacetime - x / \
                (self.k * self.c_A0 * (1 - x) ** 2)
            # Initial Guess for fsolve
            initial_guess = 0.99
            # Extract the conversion
            x[i] = fsolve(eqn, initial_guess)[0]

        # Graphing stuff
        # Conversion as a function of spacetime
        plt.plot(spacetime_span, x, 'b', label='Conversion')
        plt.legend(loc='best')
        plt.xlim(spacetime_start, spacetime_end)
        plt.xlabel('Spacetime (s)')
        plt.ylim(0, 1)
        plt.ylabel('Conversion')
        plt.grid()

        bytes_image = io.BytesIO()
        plt.savefig(bytes_image, format='png')
        bytes_image.seek(0)
        plt.close()
        return bytes_image


class CSTRTempApiHandler(Resource):
    # Permanent Constants
    # Total Concentration  - (mol/m^3)
    c_T0 = 100
    # Volume of the reactor - m^3
    volume = 0.350
    # Initial Volumetric Flowrate - m^3/s
    volumetric_flowrate = 0.002
    # Number of elements to plot
    num = 100
    # Gas Constant - cal/(mol.K)
    R = 1.9872

    # Values that are calculated from constants
    # Calculation of initial concentrations
    #   Initial concentration of A
    c_A0 = 0.5 * c_T0
    # Spacetime
    spacetime = volume / volumetric_flowrate

    def get(self):
        parser = reqparse.RequestParser()

        # Parse the query args
        parser.add_argument('lowerTemp', type=float)
        parser.add_argument('upperTemp', type=float)
        parser.add_argument('eA', type=float)
        parser.add_argument('k', type=float)
        parser.add_argument('tRef', type=float)

        args = parser.parse_args()

        # Variable inputs for the user to alter
        # Initial Temperature - K
        t_start = args.get('lowerTemp')
        if (t_start is None):
            return {
                "status": "Success",
                "message": "Lower temperature bound not provided"
            }
        # Final temperature - K
        t_end = args.get('upperTemp')
        if (t_end is None):
            return {
                "status": "Success",
                "message": "Upper temperature bound not provided"
            }
        e_a = args.get('eA')
        if (e_a is None):
            return {
                "status": "Success",
                "message": "Activation Energy not provided"
            }
        k = args.get('k')
        if (k is None):
            return {
                "status": "Success",
                "message": "Initial Rate Constant not provided"
            }
        t_ref = args.get('tRef')
        if (t_ref is None):
            return {
                "status": "Success",
                "message": "Reference Temperature not provided"
            }

        plot = self.plot(t_start, t_end, e_a, k, t_ref)

        # https://stackoverflow.com/questions/50728328/python-how-to-show-matplotlib-in-flask
        return send_file(plot,
                         attachment_filename='plot.png',
                         mimetype='image/png')

    def plot(self, t_start, t_end, e_a, k, t_ref):
        # Temperature vector
        T_span = np.linspace(t_start, t_end, self.num)

        # Conversion vector
        x = [None] * self.num

        # For loop for iterative function
        for i in range(self.num):
            # Finding the rate constants
            T = T_span[i]
            # Get the forward reaction rate constant
            k_f = k * math.exp((e_a / self.R) * ((1 / t_ref) - (1 / T)))
            # Algebraic equation
            def eqn(x): return self.spacetime - x / \
                (k_f * self.c_A0 * (1 - x) ** 2)
            # Initial Guess for fsolve
            initial_guess = 0.99
            # Extract the conversion
            x[i] = fsolve(eqn, initial_guess)[0]

        # Graphing stuff
        # Conversion as a function of spacetime
        plt.plot(T_span, x, 'b', label='Conversion')
        plt.legend(loc='best')
        plt.xlim(t_start, t_end)
        plt.xlabel('Temperature (K)')
        plt.ylim(0, 1)
        plt.ylabel('Conversion')
        plt.grid()

        bytes_image = io.BytesIO()
        plt.savefig(bytes_image, format='png')
        bytes_image.seek(0)
        plt.close()
        return bytes_image


class CSTRVarCoApiHandler(Resource):
    # Permanent Constants
    # Lower volumetric flowrate (m^3/s)
    flow_start = 0.00001
    # Upper volumetric flowrate (m^3/s)
    flow_end = 10
    # Volume of CSTR being investigated (m^3)
    volume = 0.350
    # Total Concentration  - (mol/m^3)
    c_T0 = 100
    # Rate Constant - (m^3/mol.s)
    k = 0.00001
    # Number of elements to plot
    num = 100

    # Values that are calculated from constants
    # Calculation of initial concentrations
    #   Initial concentration of A
    c_A0 = 0.5 * c_T0
    spacetime_start = volume / flow_start
    spacetime_end = volume / flow_end
    # Temperature vector
    spacetime_span = np.linspace(spacetime_start, spacetime_end, num)

    def get(self):
        parser = reqparse.RequestParser()

        # Parse the query args
        parser.add_argument('coefficient', type=float)

        args = parser.parse_args()

        # Variable inputs for the user to alter
        coefficient = args.get('coefficient')
        if (coefficient is None):
            return {
                "status": "Success",
                "message": "Activation Energy not provided"
            }

        plot = self.plot(coefficient)

        # https://stackoverflow.com/questions/50728328/python-how-to-show-matplotlib-in-flask
        return send_file(plot,
                         attachment_filename='plot.png',
                         mimetype='image/png')

    def plot(self, coefficient):

        # Conversion vector
        x = [None] * self.num

        # Basis Vector
        conversion_basis = [None] * self.num
        def basis_eqn(x, st): return self.k * st - x / ((1 - x))

        if (coefficient == 1):
            # k.tau = x_A/(c_A0.(1-x_A)^2)
            base_eqn = basis_eqn
        else:
            # k.tau.c_A0^n = (x_A/(1 - x_A)).(1/(1-n.x_A)^n))
            def base_eqn(x, st): return self.k * st * (self.c_A0 **
                                                       (coefficient - 1)) - x / ((1 - x) ** coefficient)

        # Conversion vector
        x = [None] * self.num

        # For loop for iterative function
        for i in range(self.num):
            spacetime = self.spacetime_span[i]
            # Algebraic equation
            def eqn(x): return base_eqn(x, spacetime)
            # Initial Guess for fsolve
            initial_guess = 0.99
            # Extract the conversion
            x[i] = fsolve(eqn, initial_guess, xtol=1e-10)[0]
            if coefficient == 1:
                conversion_basis[i] = x[i]
            else:
                def basis_equation(x): return basis_eqn(x, spacetime)
                conversion_basis[i] = fsolve(basis_equation, initial_guess)[0]

        # Graphing stuff
        plt.plot(self.spacetime_span, conversion_basis,
                 'b', label='Coefficient of A = 1')
        label = 'Coefficient of A = {}'.format(
            '{:f}'.format(coefficient).rstrip('.0'))
        plt.plot(self.spacetime_span, x, 'r', label=label)
        plt.legend(loc='best')
        plt.xlim(self.spacetime_end, self.spacetime_start)
        plt.xlabel('Spacetime (s)')
        plt.ylim(0, 1)
        plt.ylabel('Conversion')
        plt.grid()

        bytes_image = io.BytesIO()
        plt.savefig(bytes_image, format='png')
        bytes_image.seek(0)
        plt.close()
        return bytes_image
