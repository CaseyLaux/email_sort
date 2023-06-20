import React, { useState } from 'react';
import axios from 'axios';
import './SignupPage.css'; // Import your CSS

const SignupPage = () => {
    const [user, setUser] = useState({username: '', email: '', password: ''});

    const handleChange = e => {
        setUser({...user, [e.target.name]: e.target.value});
    }

    const handleSubmit = async e => {
        e.preventDefault();

        try {
            const response = await axios.post('http://localhost:8081/api/v1/users', user);

            if(response.status === 201) {
                alert('User created successfully');
                window.location = "/login"; // Redirect to login page
            }
        } catch (error) {
            if(error.response.status === 409) {
                alert('Username already exists');
            }
            if(error.response.status === 406) {
                alert('Please include the correct fields!');
            }
        };
    }

    return (
        <div className="signup-container">
            <h1 className="app-name">Siemless Email</h1>
            <form className="signup-form" onSubmit={handleSubmit}>
                <h2>Sign Up</h2>
                <label>Username:</label>
                <input type="text" name="username" onChange={handleChange} required />
                <label>Email:</label>
                <input type="email" name="email" onChange={handleChange} required />
                <label>Password:</label>
                <input type="password" name="password" onChange={handleChange} required />
                <button type="submit">Sign Up</button>
            </form>
        </div>
    );
}

export default SignupPage;
