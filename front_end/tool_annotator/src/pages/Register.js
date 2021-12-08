import React, { useState } from "react";
import { useHistory } from 'react-router-dom';
import AuthService from '../services/auth.service';

function Register() {
	const [first_name, setFirst_name] = useState('');
	const [last_name, setLast_name] = useState('');
	const [email, setEmail] = useState('');
	const [password, setPassword] = useState('');
	const history = useHistory();
	const [ok, setOk] = useState(false);
	const [message, setMessage] = useState('');

	const changeFirstName = event => {
		setFirst_name(event.target.value)
	}

	const changeLastName = event => {
		setLast_name(event.target.value)
	}

	const changeEmail = event => {
		setEmail(event.target.value)
	}

	const changePassword = event => {
		setPassword(event.target.value)
	}

	const handleSignUp = () => {
		setMessage("");
		setOk(false);

		AuthService.register(first_name, last_name, email, password).then(
			(response) => {
				console.log('Response:' + JSON.stringify(response, null, 2));
				setMessage(response.data.message);
				setOk(true);
			},
			(error) => {
				const resMessage = (error.response && error.response.data && error.response.data.message) || error.message || error.toString();
	  
				setMessage(resMessage);
				setOk(false);
			}
		)
		history.push('/');
	}

	return (
		<form>
			<h3>Tạo tài khoản mới</h3>

			<div className="form-group">
				<label>Tên</label>
				<input type="text" 
					className="form-control" 
					placeholder="First name" 
					onChange={changeFirstName}
				/>
			</div>

			<div className="form-group">
				<label>Họ</label>
				<input type="text" 
					className="form-control" 
					placeholder="Last name" 
					onChange={changeLastName}
				/>
			</div>

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

			<button type="submit" 
				className="btn btn-primary btn-block"
				onClick={handleSignUp}
			>
				Sign Up
			</button>
			<p className="forgot-password text-right">
				Already registered <a href="#">sign in?</a>
			</p>

			{message && (
				<div className="form-group">
					<div
						className={ ok ? "alert alert-success" : "alert alert-danger" }
						role="alert"
					>
					{message}
					</div>
				</div>
          	)}

		</form>
	);
}

export default Register;