import React from 'react';

const EmailList = ({ emails, setCurrentEmail }) => {
  return (
    <div>
      {emails.map((email, index) => (
        <button key={index} onClick={() => setCurrentEmail(email)}>
          {email.email_sender} - {email.email_subject}
        </button>
      ))}
    </div>
  );
};

export default EmailList;
