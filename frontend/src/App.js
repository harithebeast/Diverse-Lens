import React, { useState, useEffect } from "react";
import Preloader from "../src/components/Pre";
import Navbar from "./components/Navbar";
import Homesearch from "./homesearch.js";
import Home from "./components/Home/Home.js";
import Login from './login.js';
import Signup from './signup.js';


import About from "./about.js"







import {
  BrowserRouter as Router,
  Route,
  Routes,
  Navigate
} from "react-router-dom";
import ScrollToTop from "./components/ScrollToTop";
import "./style.css";
import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";

function App() {
  const [load, upadateLoad] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      upadateLoad(false);
    }, 1200);

    return () => clearTimeout(timer);
  }, []);
  
  
  
  

  return (
    <Router>
      <Preloader load={load} />
      <div className="App" id={load ? "no-scroll" : "no-scroll"}>
        <Navbar />
        <ScrollToTop />
        <Routes>
        <Route path="/" element={<Home />} />
          <Route path="/Homesearch" element={<Homesearch />} />
          
          <Route path="/About" element={<About />} />
          
          
          <Route path="/Signup" element={<Signup />} />
          
          
          
          <Route path="/Login" element={<Login />} />
        </Routes>
       
      </div>
    </Router>
  );
}

export default App;
