import React, { useState, useEffect } from 'react';
import EmailList from './EmailList';

const SortedInbox = () => {
  const [emails, setEmails] = useState([]);

  useEffect(() => {
    async function loadEmails() {
      try {
        const response = await fetch('https://serve.siemlessemail.com/api/get-emails');
        const data = await response.json();
        setEmails(data.user_sorted_emails);
      } catch (error) {
        console.error('Error loading emails:', error);
      }
    }

    loadEmails();
  }, []);

  return (
    <div>
      <h1>Sorted Inbox</h1>
      <EmailList emails={emails} />
    </div>
  );
};

export default SortedInbox;
