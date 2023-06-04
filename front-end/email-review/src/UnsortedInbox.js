import React, { useState, useEffect } from 'react';
import EmailList from './EmailList';

const UnsortedInbox = () => {
  const [emails, setEmails] = useState([]);
  const [currentEmail, setCurrentEmail] = useState(null);

  useEffect(() => {
    async function loadEmails() {
      try {
        const response = await fetch('http://localhost:3001/api/get-emails');
        const data = await response.json();
        setEmails(data.user_unsorted_emails);
      } catch (error) {
        console.error('Error loading emails:', error);
      }
    }

    loadEmails();
  }, []);

  return (
    <div>
      <h1>Unsorted Inbox</h1>
      <EmailList emails={emails} setCurrentEmail={setCurrentEmail}/>
    </div>
  );
};

export default UnsortedInbox;
