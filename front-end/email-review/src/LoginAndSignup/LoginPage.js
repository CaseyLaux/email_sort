import React, { useState } from 'react';
import axios from 'axios';
import { Link, useNavigate } from 'react-router-dom';
import './LoginPage.css';

const LoginPage = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const navigate = useNavigate();

    const handleSubmit = async (event) => {
        event.preventDefault();

        const userCredentials = {
            username: username,
            password: password
        };

        console.log(userCredentials);
        
        axios.post('http://127.0.0.1:8081/api/v1/login', userCredentials, {
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (response.data.access_token) {
                localStorage.setItem('jwt', response.data.access_token);
                navigate("/");
            } else {
                console.log(response);
            }
        })
        .catch(error => {
            if (error.response && error.response.status === 401) {
                alert('Username or password incorrect');
            } else {
                console.log(error); 
            }
        });
    };

    return (
        <div className="login-container">
            <h1 className="app-name">Siemless Email</h1>
            <form className="login-form" onSubmit={handleSubmit}>
                <h2>Login</h2>
                <label>Username:</label>
                <input type="username" value={username} onChange={(e) => setUsername(e.target.value)} required />
                <label>Password:</label>
                <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
                <button type="submit">Login</button>
                <p>Don't have an account? <Link to="/signup">Sign up here</Link></p>
            </form>
        </div>
    );
}

export default LoginPage;
