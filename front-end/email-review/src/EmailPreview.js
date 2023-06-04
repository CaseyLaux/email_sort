import React from 'react';

const EmailPreview = ({ email, selectEmail }) => {
  const { subject, sender } = email;  // Adjust these to match your actual email data structure

  return (
    <div className="email-preview" onClick={() => selectEmail(email)}>
      <div className="email-subject">{subject}</div>
      <div className="email-sender">{sender}</div>
    </div>
  );
};

export default EmailPreview;
