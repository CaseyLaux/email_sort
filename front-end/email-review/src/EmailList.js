import React from 'react';

const EmailList = ({ emails, setCurrentEmail }) => {
  return (
    <div>
      {emails.map((email, index) => (
        <button key={index} onClick={() => setCurrentEmail(email)}>
          {email.email_subject} - {email.email_sender}
        </button>
      ))}
    </div>
  );
};

export default EmailList;
