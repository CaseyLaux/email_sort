import React, { useState } from 'react';
import axios from 'axios';

const LoginPage = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();

        try {
            const response = await axios.post('http://localhost:3001/api/login', { email, password });

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
            <label>Email:</label>
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
            <label>Password:</label>
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
            <button type="submit">Login</button>
        </form>
    );
}

export default LoginPage;
