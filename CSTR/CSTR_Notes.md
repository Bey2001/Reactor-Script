# Quick Start
Open a terminal or IDE that has Python support
Command to run if libraries not presently installed
```
python -m pip install --user numpy scipy matplotlib
```
If you are having issues with your $PATH variable, add resulting directory to $PATH through the guide:
https://fabianlee.org/2021/12/23/vscode-add-a-directory-to-the-terminal-path/:~:text=From%20the%20main%20menu%2C%20go,integrated.

If in a terminal, navigate to the same directory that the files are housed in.  Run any file with 
```
python <file name>
```

For live graphs, look into matplotlib.pyplot.ion

# Introduction
This file is a detailed design description of all of the CSTR_*.py scripts I 
made as my Honors project with Dr. Karim for CHE 3184.  These were a lot of fun 
to make, and an exciting part of a series of chemical engineering applets I am 
making to help make learning more intuitive.  

This file is separated into the actual design of the files, and any issues I 
noticed when I was creating and testing the scripts.  Those issues may be 
updated in the future, and the files redesigned, but this is a starting point 
in this process!


# Design
All of these scripts borrow from HW8Q5 for the reaction.  This reaction is only augmented in CSTR_Epsilon.py, where the coefficient of B in the reaction equation is the subject of investigation, leading to the rate law also changing.

* Isothermal Spacetime - CSTR_Spacetime.py
    * Libraries
        * scipy.optimize.fsolve
        * matplotlib.pyplot
        * numpy
    * Variable inputs (to be implemented later)
        * k_f
        * c_T0
        * Volume
        * volumetric_flow_low
        * volumetric_flow_high
    * Functions
    * Output
        *Graph showing the conversion through the reactor v. spacetime
* Isothermal Temperature - CSTR_Temp.py
    * Libraries
        * scipy.optimize.fsolve
        * matplotlib.pyplot
        * numpy
    * Variable inputs (to be implemented later)
        * Ea_f
        * T0
        * k_f0
        * Tstart
        * Tend
        * c_T0
        * Volume
        * volumetric_flowrate
    * Functions
        * k_f_fun(T)
    * Output
        * Graph showing the isothermal conversion through the reactor v. temperature
* Isohermal Epsilon - CSTR_Epsilon.py
    * Libraries
        * scipy.optimize.fsolve
        * matplotlib.pyplot
        * numpy
    * Variable inputs (to be implemented later)
        * k_f
        * coefficient_start
        * coefficient_end
        * c_T0
        * Volume
        * volumetric_flowrate
    * Functions
    * Output
        * Graph showing the conversion through the reactor v. coefficient of B
* Adiabatic Operation - CSTR_Adiabatic.py
    * Libraries
        * scipy.optimize.fsolve
        * matplotlib.pyplot
        * numpy
        * math
    * Variable inputs (to be implemented later)
        * delta_H_A
        * cp_A
        * delta_H_B
        * cp_B
        * delta_H_C
        * cp_C
        * Ea_f
        * T0
        * k_f0
        * Tstart
        * Tend
        * c_T0
        * Volume
        * volumetric_flowrate
    * Functions
        * conversion_fun(T)
    * Output
        * Graph showing the adiabatic conversion through the reactor v. temperature
* Operating with Heat Exchanger - CSTR_Heat_Exchanger.py
    * Libraries
        * scipy.optimize.fsolve
        * matplotlib.pyplot
        * numpy
        * math
    * Variable inputs (to be implemented later)
        * delta_H_A
        * cp_A
        * delta_H_B
        * cp_B
        * delta_H_C
        * cp_C
        * U
        * A
        * T_A
        * Ea_f
        * T0
        * k_f0
        * Tstart
        * Tend
        * c_T0
        * Volume
        * volumetric_flowrate
    * Functions
        * conversion_fun(T)
    * Output
        * Graph showing the conversion with a heat exchanger through the reactor v. temperature




# Issues
    5/9/2022
    A big issue present in all the CSTR_*.py files is the use of fsolve.  
    Currently, this is the best numerical solver I know how to use (and from 
    the internet, the best one there is right now).  The issues come that it 
    does not have a high tolerance to get close enough to the necessary 
    solutions, and largely fails when dealing outside of certain "acceptable" 
    ranges and ends up breaking the curves and shapes down into jumbled messes, 
    oftentimes missing much of the data that should be there.  I recommend 
    looking into different packages or different functions in optimization to 
    get better data.
        One solution to this issue could be increasing the tolerance of the 
        solver itself, changing some parameters of the function.  This may or 
        may not have the desired effect, so I cautioned away from wasting time 
        with experimentation.  
        
        In truth, the best solution may just be to impose limitations on user 
        input if nothing found can possible improve its performance.