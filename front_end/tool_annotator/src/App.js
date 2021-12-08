import './App.css';
import '../node_modules/bootstrap/dist/css/bootstrap.min.css';
import Register from './pages/Register';
import Login from './pages/Login';
import Logout from './pages/Logout';
import Profile from './pages/Profile';
import UploadBook from './pages/UploadBook';
import ListBook from './pages/ListBook';
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";
import AuthService from "./services/auth.service";

import {Admin} from 'react-admin';


function App() {
  const currentUser = AuthService.getCurrentUser();

    return (
    <Router>
      <div className="App">
        <nav className="navbar navbar-expand-lg navbar-light fixed-top">
          <div className="container">
            <Link className="navbar-brand" to={"/sign-in"}>Công cụ</Link>
            <div className="collapse navbar-collapse" id="navbarTogglerDemo02">
            {!currentUser 
              ? <ul className="navbar-nav ml-auto">
                  <li className="nav-item">
                  <Link className="nav-link" to={"/sign-in"}>Đăng nhập</Link>
                  </li>
                  <li className="nav-item">
                  <Link className="nav-link" to={"/sign-up"}>Đăng ký</Link>
                  </li>
              </ul>
              : <ul className="navbar-nav ml-auto">
                <li className="nav-item">
                  <Link className="nav-link" to={"/profile"}>{currentUser.name}</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to={"/logout"}>Logout</Link>
                </li>
                </ul> 
            }
            </div>
          </div>
        </nav>
  
        <div className="auth-wrapper">
          <div className="auth-inner">
            <Switch>
              <Route exact path='/' component={UploadBook} />
              <Route path="/sign-in" component={Login} />
              <Route path="/sign-up" component={Register} />
              <Route path="/profile" component={Profile} />
              <Route path="/logout" component={Logout} />
              <Route path="/listbook" component={ListBook} />
            </Switch>
          </div>
        </div>
      </div></Router>
    );
}

export default App;
