import React from "react";

import './Info.css'


function Info() {
    return (
        <header className="App-header">
            <h1>
                ChE - Suite Help
            </h1>
            <div className="main"> 
                <h2>What is this?</h2>
                <p align="left">
                This app is software to let students explore some very trivial reactions while varying different variables that go into designing reactors.  Note that this only covers a general, albeit limited, portion of topics covered in class, and goes no further than what is covered.  This is why there is a discrepancy in the functionality available for PFRs compared to CSTRs.</p>
                <h2>How do I get started?</h2>
                <p align="left">Users need only click on the Navbar to get the reactor type they wish to explore, then the type of analysis they wish to conduct.  From there, you need to enter the values you wish to use in your analysis (within the bounds delineated by the error helper messages under the text form fields), then press calculate.</p>
                <h2>What are this software's limitations?</h2>
                <p align="left">The types of calculations that go into finding the conversion of species using CSTRs and PFRs are complicated, but relatively easy to solve.  You can use algebra to analyze CSTRs and basic integral calculus for PFRs.  This is not to say that EVERY reaction can be easily analyzed, but the ones chosen for this app for demonstration purposes are easily analyzed.
                <br/>
                &emsp; The backend for this app, that which does the calculations, is in Python, and the user interface you are using to access this app is built in JavaScript.  The biggest caveat actually exists in finding zeroes for CSTR analysis, since the Python fsolve is relatively weak and poor at finding zeroes of complex algebraic equations.  
                </p>
            </div>
        </header>
    );
}

export default Info;