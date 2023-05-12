import React, { useState, useEffect } from "react";

const EmailList = () => {
  const [emails, setEmails] = useState([]);
  const [emailContents, setEmailContents] = useState([]);

  useEffect(() => {
    fetch("/index.json")
      .then((response) => response.json())
      .then((data) => {
        setEmails(data);
        fetchEmailContents(data);
      });
  }, []);

  const fetchEmailContents = async (emailFiles) => {
    const emailPromises = emailFiles.map((emailFile) =>
      fetch(`/human_sorted/${emailFile}`).then((response) => response.text())
    );
    const contents = await Promise.all(emailPromises);
    setEmailContents(contents);
  };

  return (
    <div>
      <h2>Emails</h2>
      <ul>
        {emailContents.map((content, index) => (
          <li key={index}>
            <div>
              <strong>Email {index + 1}</strong>
            </div>
            <pre>{content}</pre>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default EmailList;
