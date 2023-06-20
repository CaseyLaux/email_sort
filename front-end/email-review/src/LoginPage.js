import React, { useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import './LoginPage.css'; // Import the new CSS

const LoginPage = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();

        try {
            console.log(username, password)
            const response = await axios.post('http://localhost:8081/api/v1/login', { username, password });
            
            if (response.data.token) {
                localStorage.setItem('jwt', response.data.token);
                window.location = "/"; // Redirect to home page or dashboard
            } else {
                // Handle error here (invalid credentials)
            }
        } catch (error) {
            // Handle error here (e.g. server error)
        }
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
