import React from 'react';
import DOMPurify from 'dompurify'; // Don't forget to install this package using npm

const EmailDetail = ({ email, onClose }) => {
  console.log('EmailDetail received email:', email);

  // Use html_body if it exists, otherwise use body
  const bodyContent = email.html_body || email.body;

  // Sanitize the body content
  const sanitizedHTML = DOMPurify.sanitize(bodyContent);

  return (
    <div className="email-detail">
      <button onClick={onClose}>Close</button>
      <h2>{email.subject}</h2>
      <div dangerouslySetInnerHTML={{ __html: sanitizedHTML }} />
      {/* ... any other email fields you want to display ... */}
    </div>
  );
};

export default EmailDetail;
