from flask import send_file
from flask_restful import Resource, reqparse
import matplotlib.pyplot as plt
import numpy as np
import io
# Function for finding 0s to algebraic equations
import scipy.integrate as integrator
import math


class PFRAdiabaticApiHandler(Resource):

  ### Permanent Constants
  # Forward Activation Energy - cal/mol
  Ea_f = 10000
  # Temperature for original k values - K
  T0 = 300
  # Rate Constant at T0 K - (m^3/mol.s)
  k_f0 = 0.00001 # 0.01 L/mol.s
  # Total Concentration - (mol/m^3)
  c_T0 = 100 # 0.1 M
  # Volume of the reactor - m^3
  volume = 0.350 #350 L
  # Initial Volumetric Flowrate - (m^3/s)
  volumetric_flowrate = 0.002 #2 L/s
  # Gas Constant - cal/(mol.K)
  R = 1.9872
  # Number of elements to plot
  num = 101

  ### Constants calculated from other constants
  # Initial Concentrations
  c_A0 = 0.5 * c_T0
  c_B0 = 0.5 * c_T0
  # Initial molar flowrates - mol/min
  #   Molar flowrate of A
  F_A0 = volumetric_flowrate*c_A0
  #   Molar flowrate of B
  F_B0 = volumetric_flowrate*c_B0

  ### Mass Balance vectors - Length 101 to have clean numbers
  # These are actually constant, regardless of values input by user
  #   Conversion vector for the mass balance 
  #   - Constant across the temperature, regardless of thermodynamic properties
  #   - Calculated by using the original PFR_Adiabatic script from 300 to 1000K
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
          972,  979,  986,  993, 1000,]

  def get(self):
    parser = reqparse.RequestParser()

    # Parse the query args
    parser.add_argument('lowerTemp', type=float)
    parser.add_argument('upperTemp', type=float)
    parser.add_argument('cA', type=float)
    parser.add_argument('hfA', type=float)
    parser.add_argument('cB', type=float)
    parser.add_argument('hfB', type=float)
    parser.add_argument('cC', type=float)
    parser.add_argument('hfC', type=float)

    args = parser.parse_args()

    ###Variable inputs for the user to alter
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

    plot = self.plot(t_start, t_end, delta_H_A, cp_A, delta_H_B, cp_B, delta_H_C)

    # https://stackoverflow.com/questions/50728328/python-how-to-show-matplotlib-in-flask
    return send_file(plot,
                    attachment_filename='plot.png',
                    mimetype='image/png')

  def plot(self, t_start, t_end, delta_H_A, cp_A, delta_H_B, cp_B, delta_H_C):
    ### Values that are calculated from parameters
    # Total heat of reaction - Must be greater than 0
    delta_H_r = delta_H_C - delta_H_A - delta_H_B
    #Summing all the values of FiCpi for adiabatic calculations
    sum_flow_times_cp = self.F_A0*cp_A + self.F_B0*cp_B

    #ODE function for changing flow rates
    def energy_balance(Volume, F):
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

        #Unpacking the next iteration of values
        F_A, F_B, T, v = F
        #Concentration of A
        c_A = F_A/v 
        #Concentration of B
        c_B = F_B/v 

        #Getting the forward reaction rate constant
        k_f = self.k_f0 * math.exp((self.Ea_f / self.R) * ((1 / self.T0) - (1/T)))

        #Rate at this particular point in the volume
        r = k_f*c_A*c_B

        #List of differentials to be returned
        dFdV = [-r, -r, -r * delta_H_r/sum_flow_times_cp, 0]
        return dFdV

    # Vector spanning from 0 to the volume given
    volume_span = [0, self.volume]
    # The initial conditions to be fed into the ODE Solver
    initial_conditions = [self.F_A0, self.F_B0, self.T0, self.volumetric_flowrate]

    # Using integrate.solve_ivp to solve the energy balance equations
    solution = integrator.solve_ivp(energy_balance, volume_span, initial_conditions, method='BDF')
    # Pulling out the flowrate of B
    F_A0_arr = solution.y[0]

    ### Energy Balance vectors
    # Pulling out the temperature vector
    T_EB = solution.y[2]
    # Calculating the conversion vector
    x_EB = 1 - F_A0_arr/F_A0_arr[0]
    ### Graphing stuff
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

class PFRSpacetimeApiHandler(Resource):
  ### Other numerical values
  # Rate Constant - (m^3/mol.s)
  k = 0.00001
  # Total Concentration - (mol/m^3)
  c_T0 = 100
  # Number of elements to plot
  num = 101



  ### Values that are calculated from parameters
  # Calculation of initial concentrations
  c_A0 = 0.5 * c_T0
  c_B0 = 0.5 * c_T0

  def get(self):
    parser = reqparse.RequestParser()

    # Parse the query args
    parser.add_argument('lowerFlowrate', type=float)
    parser.add_argument('upperFlowrate', type=float)
    parser.add_argument('volume', type=float)

    args = parser.parse_args()

    ### Variable inputs for the user to alter
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
    #ODE function for changing flow rates
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

        #Unpacking the flowrates at the current volume
        F_A, F_B = F
        #Concentration of A
        c_A = F_A/volumetric_flowrate 
        #Concentration of B
        c_B = F_B/volumetric_flowrate 

        #Rate at this particular point in the volume
        r = self.k*c_A*c_B

        #List of differentials to be returned
        dFdV = [-r, -r]
        return dFdV

    #Programming of the ODEsolver function
    # Function definition replicating ode15s
    ode15s = integrator.ode(deriv)
    ode15s.set_integrator('vode', method='bdf', order=15, nsteps=1e8)

    #Function to house the use of the ODE solver
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
        #The initial conditions to be fed into the ODE Solver
        F_0 = [volumetric_flowrate*self.c_A0, volumetric_flowrate*self.c_B0]
        #Setting the initial conditions for the ODE Solver
        ode15s.set_initial_value(F_0, 0)
        #Setting up the parameters to be fed into the ODE Solver
        ode15s.set_f_params(volumetric_flowrate)
        #Only returns the last iteration of ode15s
        sol = ode15s.integrate(volume)
        array = [F_0, [sol[0], sol[1]]]
        return array

    #Volumetric flow vector
    #   Spans from the first volumetric flowrate specified by the user to the last, 
    #   separated by the number of points specified (1000)
    volumetric_flow_span = np.linspace(flow_start, flow_end, 
        self.num) 

    #Conversion vector
    x = [None] * self.num

    #For loop for iterative function
    for i in range(self.num):
        #Feed in the current volumetric flowrate
        iter = iterative(volumetric_flow_span[i])
        #Extract the conversion
        x[i] = (iter[0][1] - iter[1][1])/iter[0][1]

    #Getting spacetime from the volumes
    spacetime = np.divide(volume, volumetric_flow_span)

    ### Graphing stuff
    #Conversion as a function of spacetime
    plt.plot(spacetime, x, 'b', label='Conversion')    
    plt.legend(loc='best')
    plt.xlim(volume/flow_end, volume/flow_start)
    plt.xlabel('Spacetime (s)')
    plt.ylim(0, 1)
    plt.ylabel('Conversion')
    plt.grid()

    bytes_image = io.BytesIO()
    plt.savefig(bytes_image, format='png')
    bytes_image.seek(0)
    plt.close()
    return bytes_image

class PFRTempApiHandler(Resource):
  ### Permanent Constants
  # Temperature for original k values - K
  T0 = 300
  # Total Concentration - (mol/m^3)
  c_T0 = 100 # 0.1 M
  # Volume of the reactor - m^3
  Volume = 0.350 #350 L
  # Initial Volumetric Flowrate - (m^3/s)
  volumetric_flowrate = 0.002 #2 L/s
  # Gas Constant - cal/(mol.K)
  R = 1.9872
  # Number of elements to plot
  num = 101

  ### Values that are calculated from constants
  # Initial Concentration of A and B
  c_A0 = 0.5 * c_T0
  c_B0 = 0.5 * c_T0
  # Spacetime
  spacetime = Volume / volumetric_flowrate
  # Initial Molar Flowrates of A and B
  F_A0 = c_A0 * volumetric_flowrate
  F_B0 = c_B0 * volumetric_flowrate

  def get(self):
    parser = reqparse.RequestParser()

    # Parse the query args
    parser.add_argument('lowerTemp', type=float)
    parser.add_argument('upperTemp', type=float)
    parser.add_argument('eA', type=float)
    parser.add_argument('k', type=float)
    parser.add_argument('tRef', type=float)

    args = parser.parse_args()

    ### Variable inputs for the user to alter
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
        c_A = F_A/self.volumetric_flowrate 
        # Concentration of B
        c_B = F_B/self.volumetric_flowrate 

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
        k_f = k * math.exp((e_a / self.R)*((1 / t_ref) - (1 / T)))
        # Finding the reverse k value
        F_0 = [self.F_A0, self.F_B0]
        # Setting the initial conditions for the ODE Solver
        ode15s.set_initial_value(F_0, 0)
        # Setting up the parameters to be fed into the ODE Solver
        ode15s.set_f_params(k_f)
        # Only returns the last iteration of ode15s
        sol = ode15s.integrate(self.Volume)
        array = [F_0, [sol[0], sol[1]]]
        return array

    # Temperature vector
    #   Spans from the start temperature specified to the end temperature 
    #   specified, separated by the number of points specified (1000)
    T_span = np.linspace(t_start, t_end, self.num) 

    # Conversion vector
    x = [None] * self.num

    # For loop for iterative function
    for i in range(self.num):
        # Feed in the current temperature to be evaluated
        iter = iterative(T_span[i])
        # Extract the conversion from the end
        x[i] = (iter[0][1] - iter[1][1])/iter[0][1]

    ### Graphing stuff
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

class PFRVarCoApiHandler(Resource):
    ### Permanent Constants
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

    ### Values that are calculated from constants
    # Calculation of initial concentrations
    #   Initial concentration of A
    c_A0 = 0.5 * c_T0
    c_B0 = 0.5 * c_T0
    spacetime_start = volume / flow_start
    spacetime_end = volume / flow_end
    # Temperature vector
    spacetime_span = np.linspace(spacetime_start, spacetime_end, num)

    conversion_basis = [0.9459456819633106, 0.9454242099861352, 0.9448925792185238, 0.9443504888388962, 0.9437976271632356, 0.943233671071089, 0.942658282461978, 0.9420711096774365, 0.9414717904555135, 0.9408599418908397, 0.9402351627344165, 0.939597046791151, 0.9389451580456484, 0.9382790388291344, 0.9375982283522132, 0.9369022305772017, 0.9361905266001553, 0.9354625849499286, 0.9347178419047603, 0.9339557077538695, 0.9331755685835744, 0.9323767782621104, 0.9315586607799408, 0.9307205050188039, 0.9298615668083108, 0.9289810620757131, 0.9280781696130093, 0.9271520231071709, 0.9262017140050581, 0.9252262829055174, 0.9242247220514175, 0.9231959656997392, 0.92213889319028, 0.9210523164102522, 0.9199349856646863, 0.9187855723117252, 0.9176026780853579, 0.9163848139301336, 0.9151304101660706, 0.9138377944356145, 0.9125051970945526, 0.9111307311708882, 0.909712400711437, 0.9082480612281765, 0.9067354494219388, 0.9051721194251173, 0.9035554907990088, 0.901882774429094, 0.9001510092993144, 0.8983570087084405, 0.8964973619247629, 0.8945684003756833, 0.8925661739468943, 0.890486427703738, 0.8883245709956753, 0.8860756437885755, 0.8837342779536708, 0.8812946552438842, 0.8787504587736301, 0.8760948177499593, 0.8733202426291657, 0.8704185561474554, 0.8673808241497564, 0.864197250844646, 0.8608570901311107, 0.8573484837514791, 0.8536583537495859, 0.8497722318383304, 0.8456740660078944, 0.8413460222877002, 0.8367682184343626, 0.8319183912533238, 0.8267715490946894, 0.8212995482383247, 0.8154705765751966, 0.8092485262071847, 0.8025922299958015, 0.7954545815289086, 0.7877814492482593, 0.779510238350729, 0.7705681181156898, 0.7608699794013326, 0.7503159159810814, 0.7387875052979261, 0.7261428890498782, 0.712211487774843, 0.6967865155275922, 0.6796145133795515, 0.6603805979249234, 0.6386899022306443, 0.6140403764163188, 0.585780171407869, 0.5530550357402704, 0.5147139042461059, 0.4691771009245152, 0.414210688277733, 0.3465455301501841, 0.2612058884719971, 0.1502267981133905, 1.7499241517157317e-05]

    def get(self):
        parser = reqparse.RequestParser()

        # Parse the query args
        parser.add_argument('coefficient', type=float)

        args = parser.parse_args()

        ### Variable inputs for the user to alter
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

        #ODE function for changing flow rates
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

            #Unpacking the flowrates at the current volume
            F_A, F_B = F
            #Concentration of A
            c_A = F_A/flowrate
            #Concentration of B
            c_B = F_B/flowrate

            #Rate at this particular point in the volume
            r = self.k * c_A * (c_B ** coefficient)

            #List of differentials to be returned
            dFdV = [-r, -r]
            return dFdV

        #Programming of the ODEsolver function
        # Function definition replicating ode15s
        ode15s = integrator.ode(deriv)
        ode15s.set_integrator('vode', method='bdf', order=15, nsteps=1e8)

        #Function to house the use of the ODE solver
        # Generates the final conversions per iteration using different coefficients of 
        #   R
        def iterative(spacetime):
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
            flowrate = self.volume / spacetime

            F_0 = [flowrate*self.c_A0, flowrate * self.c_B0]
            ode15s.set_initial_value(F_0, 0)
            ode15s.set_f_params(flowrate)
            #Only returns the last iteration of ode15s
            sol = ode15s.integrate(self.volume)
            array = [F_0, [sol[0], sol[1]]]
            return array

        #Conversion vector
        x = [None] * self.num

        #For loop for iterative function
        for i in range(self.num):
            #Feed in the current volumetric flowrate
            iter = iterative(self.spacetime_span[i])
            #Extract the conversion
            x[i] = (iter[0][1] - iter[1][1])/iter[0][1]

        ### Graphing stuff
        # Conversion as a function of spacetime
        plt.plot(self.spacetime_span, self.conversion_basis, 'b', label='Coefficient of B = 1')
        label = 'Coefficient of B = {}'.format('{:f}'.format(coefficient).rstrip('.0'))
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