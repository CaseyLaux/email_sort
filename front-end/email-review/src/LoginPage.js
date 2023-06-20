import React, { useState } from 'react';
import axios from 'axios';

const LoginPage = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();

        try {
            const response = await axios.post('http://localhost:3001/api/login', { username, password });

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
        <form onSubmit={handleSubmit}>
            <h2>Login</h2>
            <label>username:</label>
            <input type="username" value={username} onChange={(e) => setUsername(e.target.value)} required />
            <label>Password:</label>
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
            <button type="submit">Login</button>
        </form>
    );
}

export default LoginPage;
