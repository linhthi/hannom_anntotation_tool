import React, { useState } from "react";
import { useHistory } from 'react-router-dom';
import AuthService from '../services/auth.service';


function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState("");
    const history = useHistory();

    const changeEmail = (e) => {
        setEmail(e.target.value);
    };

    const changePassword = (e) => {
        setPassword(e.target.value);
    };

    const handleLogin = (e) => {
        e.preventDefault();

        setMessage("");
        setLoading(true);

        AuthService.login(email, password).then(
        (response) => {
            console.log('Response:' + JSON.stringify(response, null, 2));
            // window.location.reload();
        },
        (error) => {
            const resMessage =
            (error.response &&
                error.response.data &&
                error.response.data.message) ||
            error.message ||
            error.toString();

            setLoading(false);
            setMessage(resMessage);
        }
        );
        history.push('/profile');
    };

    return (
        <form>
            <h3>Đăng nhập</h3>

            <div className="form-group">
                <label>Email address</label>
                <input type="email" 
                    className="form-control" 
                    placeholder="Enter email" 
                    onChange={changeEmail}    
                />
            </div>

            <div className="form-group">
                <label>Password</label>
                <input type="password" 
                    className="form-control" 
                    placeholder="Enter password" 
                    onChange={changePassword}
                />
            </div>

            <div className="form-group">
                <div className="custom-control custom-checkbox">
                    <input type="checkbox" className="custom-control-input" id="customCheck1" />
                    <label className="custom-control-label" htmlFor="customCheck1">Remember me</label>
                </div>
            </div>

            <button type="submit" className="btn btn-primary btn-block" onClick={handleLogin}>
                Submit
            </button>
            {/* <p className="forgot-password text-right">
                Forgot <a href="#">password?</a>
            </p> */}
            {message && (
            <div className="form-group">
              <div className="alert alert-danger" role="alert">
                {message}
              </div>
            </div>
          )}
        </form>
    );
}

export default Login;