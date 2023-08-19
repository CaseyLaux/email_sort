import React, { useState } from 'react';
import axios from 'axios';
import './SignupPage.css'; // Import your CSS

const SignupPage = () => {
    const [user, setUser] = useState({username: '', password: '', emails: [{email: '', secret: ''}]});

    const handleUserChange = e => {
        setUser({...user, [e.target.name]: e.target.value});
    }

    const handleEmailChange = (index, e) => {
        const emails = [...user.emails];
        emails[index] = {...emails[index], [e.target.name]: e.target.value};
        setUser({...user, emails});
    }

    const addEmail = () => {
        setUser({...user, emails: [...user.emails, {email: '', secret: ''}]});
    }

    const handleSubmit = async e => {
        e.preventDefault();

        try {
            const response = await axios.post('http://127.0.0.1:8081/api/v1/users', user);

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
                <input type="text" name="username" onChange={handleUserChange} required />
                <label>Password:</label>
                <input type="password" name="password" onChange={handleUserChange} required />
                {user.emails.map((email, index) => (
                    <div key={index}>
                        <label>Email:</label>
                        <input type="email" name="email" value={email.email} onChange={e => handleEmailChange(index, e)} required />
                        <label>Secret:</label>
                        <input type="password" name="secret" value={email.secret} onChange={e => handleEmailChange(index, e)} required />
                    </div>
                ))}
                <button type="button" onClick={addEmail}>Add Email</button>
                <button type="submit">Sign Up</button>
            </form>
        </div>
    );
}

export default SignupPage;
