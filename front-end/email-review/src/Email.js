import React from 'react';

const Email = ({ email }) => {
  if (!email) {
    return <p>No email selected.</p>;
  }

  return (
    <div className="email">
      <p><strong>Subject:</strong> {email.subject}</p>
      <p><strong>From:</strong> {email.email_sender}</p>
      <p><strong>To:</strong> {email.email_recipient}</p>
      <p><strong>Date:</strong> {email.email_date}</p>
      <div
        className="email-content"
        dangerouslySetInnerHTML={{ __html: email.prompt}}
      />
    </div>
  );
};

export default Email;
