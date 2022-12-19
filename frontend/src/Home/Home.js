import React, { useState, useEffect } from "react";
import logo from '../logo.svg';
import axios from 'axios';

import './Home.css';

function Home() {
    const [getMessage, setGetMessage] = useState({})

    useEffect( () => {
      axios.get('http://localhost:5000/flask/hello').then(response => {
        console.log("SUCCCESS", response)
        setGetMessage(response)
      }).catch(error => {
        console.log(error)
      })
    }, [])
  

    return (
        <header className="App-header">
            <img src={logo} className="Home-logo" alt="logo" />
            <h1>
                ChE - Suite Home
            </h1>
            <div> {getMessage.status === 200 ?
                <h3>{getMessage.data.message}</h3>
                :
                <h3>Loading</h3>}
            </div>
        </header>
    );
}

export default Home;