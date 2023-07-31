import React, { useState, useEffect } from 'react';

const Profile = () => {
  const [user, setUser] = useState(null);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const token = localStorage.getItem('jwt');
  
  useEffect(() => {
    fetchUserProfile();
  }, []);

  const fetchUserProfile = () => {
    fetch(`https://serve.siemlessemail.com/profile`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
      .then(response => response.json())
      .then(data => setUser(data))
      .catch(err => console.log(err));
  }

  const handleEmailAndPasswordChange = (event) => {
    event.preventDefault();

    fetch(`https://serve.siemlessemail.com/email_add`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    })
      .then(response => response.json())
      .then(() => {
        setEmail('');
        setPassword('');
        fetchUserProfile();
      })
      .catch(err => console.log(err));
  };

  if (!user) return 'Loading...';

  return (
    <div>
      <h1>{user.username}'s Profile</h1>
      <p>Email: {user.email}</p>
      {/* render other user info here */}
      <form onSubmit={handleEmailAndPasswordChange}>
        <label>
          Add a new email address:
          <input type="email" value={email} onChange={e => setEmail(e.target.value)} required />
        </label>
        <label>
          <input type="password" value={password} onChange={e => setPassword(e.target.value)} required />
        </label>
        <input type="submit" value="Submit" />
      </form>
    </div>
  );
};

export default Profile;
