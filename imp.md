
Need to look into how to make material-UI components for analogous components for the prototype.  I also need to look up how to run those python functions from the app itself.

Should build the server to make the plots, then bring them to the foreground, likely through the use of BytesIO:
- Solution with transforming plots into HTML files
    - https://www.freecodecamp.org/news/how-to-embed-interactive-python-visualizations-on-your-website-with-python-and-matplotlib/
- Solution that deals with BytesIO
    - https://towardsdatascience.com/python-plotting-api-expose-your-scientific-python-plots-through-a-flask-api-31ec7555c4a8
    - https://gitlab.com/dice89/python-plotting-api/-/tree/master/python_plotting_api
- Solution that deals with frontend graph rendering
    - https://aknay.github.io/2021/01/06/build-a-react-flask-app-with-react-vis-chart-for-data-visualization.html
- Other thing
    - https://codesandbox.io/s/rm4pyq9m0o
- The first one here worked!
    - https://stackoverflow.com/questions/70281939/how-to-show-image-from-bytes

# To Do
Need to design a much simpler reaction that can just be solved algebraically instead of using calculus.  This should be a relatively straightforward analysis for an easy situation, probably with just two different reactants to simplify things for demonstration purposes only.

I also need to make a small writeup for the reaction used to be displayed for every page, in addition to the parameters that the user needs to enter. 

Need to delineate the appropriate parameters that the user can feed into the different types of analysis:
- Adiabatic
    - Lower Temperature Bound
    - Upper Temperature Bound
    - Specific Heat of Reactant A
    - Heat of Formation of Reactant A
    - Specific Heat of Reactant B
    - Heat of Formation of Reactant B
    - Specific Heat of Product C
    - Heat of Formation of Product C
        - May want to check the physics to make sure that there are no issues with the heats of formation and the activation energy; if there are, then just ensure that the appropriate difference between heats of formation is no greater than the activation energy.
- Epsilon
    - Coefficient of Reactant B
- Heat Exchanger
    - Lower Temperature Bound
    - Upper Temperature Bound
    - Heat Transfer Coefficient
    - Area of Heat Transfer
    - Surface Temperature
- Spacetime
    - Reactor Volume
    - Volumetric Flowrate
- Temperature
    - Lower Temperature Bound
    - Upper Temperature Bound
    - Activation Energy
    - Measured Rate Constant
    - Reference Temperature for Rate Constant

CSTR already has A + B -> C in the scripts, so I will have to retrofit the PFR scripts to accomodate for that, as well as doublecheck my maths for a good limit of the parameters that can be passed in.

Had to set a callback function for setState since it's an asynchronous function (Source: https://stackoverflow.com/questions/54549069/how-to-setstate-with-a-file-object).

Some suggestions for the Frontend:
- Dark Mode present for everything
- Navbar
    - Get rid of the icon
    - Fix the font of ChE-Suite
    - Left-justify the CSTR and PFR buttons
    - Make them interactive dropdown menus, rather than just buttons
    - Rename HELP to Info
- Home Menu
    - Decrease the space between paragraphs to make it a one-screen page
- Help Page --> Info Page
    - Make a section for help/access to videos
- Make a footer to credit Sam/give access to different pages from a quick point of view
- Possibly make a landing page