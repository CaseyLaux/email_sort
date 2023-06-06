import React from 'react';

const EmailDetail = ({ email, onClose }) => {
  console.log('EmailDetail received email:', email);
  return (
    <div className="email-detail">
      <button onClick={onClose}>Close</button>
      <h2>{email.subject}</h2>
      <p>{email.body}</p>
      {/* ... any other email fields you want to display ... */}
    </div>
  );
};

export default EmailDetail;
