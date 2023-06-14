import React, { useState, useEffect } from 'react';

const Email = ({ email }) => {
  const [body, setBody] = useState('');

  useEffect(() => {
    if (email) {
      const bodyContent = email.html_body ? email.html_body : email.body;
      if (bodyContent) {
        const reader = new FileReader();
        reader.onload = function(event) {
          setBody(event.target.result);
        };
        reader.readAsText(new Blob([bodyContent]));
      }
    }
  }, [email]);

  if (!email) {
    return <p>No email selected.</p>;
  }

  return (
    <div className="email">
      <p><strong>Subject:</strong> {email.email_subject}</p>
      <p><strong>From:</strong> {email.email_sender}</p>
      <p><strong>Date:</strong> {email.email_date}</p>
      <div
        className="email-content"
        dangerouslySetInnerHTML={{ __html: body }}
      />
    </div>
  );
};

export default Email;
