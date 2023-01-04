import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Home from "./Home/Home";
import Info from "./Info/Info";
import Navbar from "./Navbar/Navbar";
import CSTRAdiabatic from "./Reactors/ReactorPages/CSTR/CSTRAdiabatic";
import CSTRExchanger from "./Reactors/ReactorPages/CSTR/CSTRExchanger";
import CSTRSpacetime from "./Reactors/ReactorPages/CSTR/CSTRSpacetime";
import CSTRTemp from "./Reactors/ReactorPages/CSTR/CSTRTemp";
import CSTRVarCo from "./Reactors/ReactorPages/CSTR/CSTRVarCo";
import PFRAdiabatic from "./Reactors/ReactorPages/PFR/PFRAdiabatic";
import PFRSpacetime from "./Reactors/ReactorPages/PFR/PFRSpacetime";
import PFRTemp from "./Reactors/ReactorPages/PFR/PFRTemp";
import PFRVarCo from "./Reactors/ReactorPages/PFR/PFRVarCo";

import "./App.css";

function App() {
  return (
    <div className="App">
      <Navbar />
      <Router>
        <Routes>
          <Route exact path="/" element={<Home />} />
          <Route exact path="/cstr/adiabatic" element={<CSTRAdiabatic />} />
          <Route exact path="/cstr/exchanger" element={<CSTRExchanger />} />
          <Route exact path="/cstr/spacetime" element={<CSTRSpacetime />} />
          <Route exact path="/cstr/temperature" element={<CSTRTemp />} />
          <Route exact path="/cstr/varco" element={<CSTRVarCo />} />
          <Route exact path="/pfr/adiabatic" element={<PFRAdiabatic />} />
          <Route exact path="/pfr/spacetime" element={<PFRSpacetime />} />
          <Route exact path="/pfr/temperature" element={<PFRTemp />} />
          <Route exact path="/pfr/varco" element={<PFRVarCo />} />
          <Route exact path="/info" element={<Info />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
