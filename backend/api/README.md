# General Comments on the Backend Server

This directory holds the Controllers for the different API dealing with CSTR and PFR analysis. These two files have different classes that each represent the type of analysis to be investigated using whichever reactor the user wishes to use. The goal is to parse the parameters from the URL being accessed, and then used in creating a plot to be used in the greater analysis. Moreover, the graph is then sent back to the client-side as a BytesIO, which is effectively just a byte buffer. It is up to the frontend to then decipher these bytes as an image.
