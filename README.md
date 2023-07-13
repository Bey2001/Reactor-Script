# Reactor-Script
This repo houses the scripts I wrote for my Honors project for CHE 3184.  I plan to turn these scripts into the backend for an applet for educational purposes for chemical engineering students

For more descriptive information, check out my CSTR.md and PFR.md for details on my CSTR and PFR scripts respectively.

# Starting the Python environment
First, we need to create a new Python environment.  

If conda is not on your system already, run the following command:
```
conda install
```

Run ``conda create --name <desired name> python`` to make a new conda environment.  Then, run ``conda activate reactors``.  You should now be in the reactors python environment.

# Running publicly
- For the frontend
    - ``HOST=172.21.138.38 npm run start``
- For the backend
    - ``flask run --host=172.21.138.38``