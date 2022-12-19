import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './Components/Navbar/Navbar';
import Home from './Home/Home';
import CSTRAdiabatic from './CSTR/CSTRAdiabatic';
import CSTRVarCo from './CSTR/CSTRVarCo';
import CSTRExchanger from './CSTR/CSTRExchanger';
import CSTRSpacetime from './CSTR/CSTRSpacetime';
import CSTRTemp from './CSTR/CSTRTemp';
import PFRAdiabatic from './PFR/PFRAdiabatic';
import PFRVarCo from './PFR/PFRVarCo';
import PFRSpacetime from './PFR/PFRSpacetime';
import PFRTemp from './PFR/PFRTemp';
import Help from './Help/Help';

import './App.css';


function App() {
  return (
    <div className="App">
      <Navbar />
      <Router>
        <Routes>
          <Route exact path="/" element={<Home />} />
          <Route exact path="/help" component={<Help />} />
          <Route exact path="/cstr/adiabatic" element={<CSTRAdiabatic />} />
          <Route exact path="/cstr/exchanger" element={<CSTRExchanger />} />
          <Route exact path="/cstr/spacetime" element={<CSTRSpacetime />} />
          <Route exact path="/cstr/temperature" element={<CSTRTemp />} />
          <Route exact path="/cstr/varco" element={<CSTRVarCo />} />
          <Route exact path="/pfr/adiabatic" element={<PFRAdiabatic />} />
          <Route exact path="/pfr/spacetime" element={<PFRSpacetime />} />
          <Route exact path="/pfr/temperature" element={<PFRTemp />} />
          <Route exact path="/pfr/varco" element={<PFRVarCo />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
