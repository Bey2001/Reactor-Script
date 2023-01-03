import React from "react";
import logo from '../logo.svg';

import './Home.css';

function Home() {

    return (
        <header className="Home-header">
            <img src={logo} className="Home-logo" alt="logo" />
            <h1>
                ChE - Suite Home
            </h1>
            <h3>This app is Reactor Simulation Software for 
              Virginia Tech's Department of Chemical Engineering 
              Reactor Analysis and Design course.</h3>
        </header>
    );
}

export default Home;