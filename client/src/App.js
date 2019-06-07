import React, { Component } from 'react';
import Login from './Components/Login/Login';
import Signup from './Components/Signup/Signup'
import Fpassword from './Components/Login/Fpassword'
import {Router} from '@reach/router';
import Home from './Components/home'
import Header from './Components/home/header'
//import Openproject from './Components/openproject/background'
import About from './Components/about/about'
import './index.css';
import './style.css'
class App extends Component {
  render() {

    return (
      <div>
        <Header />
        <Router>
          <Home path = "/" />
          <Login path = "login" />
          <Fpassword path = "fpassword" />
          <Signup path = "signup" />
          <About path = "about" />
        </Router>

      </div>
         
    );
  }
}

export default App;
