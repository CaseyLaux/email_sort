import React, { useState, useEffect } from 'react';
import './EmailViewer.css';
import Email from './Email';
import EmailControls from './EmailControls';

const EmailViewer = () => {
  const [humanSortedEmails, setHumanSortedEmails] = useState([]);
  const [unsortedEmails, setUnsortedEmails] = useState([]);
  const [humanSortedIndex, setHumanSortedIndex] = useState(0);
  const [unsortedIndex, setUnsortedIndex] = useState(0);
  const [rating, setRating] = useState('');
  const [classification, setClassification] = useState('');
  const [unsortedFilenames, setUnsortedFilenames] = useState([]);
  
  const deleteEmail = async (email) => {
    const email_id = {
      ...email,
      _id: email._id.$oid,
    };
    try {
      const response = await fetch('http://localhost:3001/api/delete-email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: email_id }),
      });
  
      if (!response.ok) {
        throw new Error('Failed to delete email.');
      }
  
      // Update unsortedEmails state to remove the deleted email
      setUnsortedEmails((prevState) => prevState.filter((e) => e._id !== email._id));
  
      alert('Email deleted successfully.');
    } catch (error) {
      console.error(error);
      alert('Failed to delete email.');
    }
  };

  useEffect(() => {
    async function loadEmails() {
      try {
        const response = await fetch('http://localhost:3001/api/get-emails');
        const data = await response.json();
        console.log(data);
        setHumanSortedEmails(data.body_emails);
        setUnsortedEmails(data.unsorted_emails);
        console.log(humanSortedEmails);
        console.log(unsortedEmails);
      } catch (error) {
        console.error('Error loading emails:', error);
      }
    }

    loadEmails();
  }, []);

  const moveEmail = async (email) => {
    // Validate rating and classification inputs
    if (!rating || !classification) {
      alert('Please enter a rating and classification.');
      return;
    }
  
    // Add classification and rating to the email completion field
    const updatedEmail = {
      ...email,
      completion: `Classification: ${classification}, Rating: ${rating}`,
      _id: email._id.$oid,
    };
  
    try {
      const response = await fetch('http://localhost:3001/api/move-email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: updatedEmail }),
      });
  
      if (!response.ok) {
        throw new Error('Failed to move email.');
      }
  
      // Update unsortedEmails state to remove the moved email
      setUnsortedEmails((prevState) => prevState.filter((e) => e._id !== email._id));
  
      // Reset rating and classification inputs
      setRating('');
      setClassification('');
  
      alert('Email moved successfully.');
    } catch (error) {
      console.error(error);
      alert('Failed to move email.');
    }
  };
  

  const changeIndex = (currentIndex, emailsLength, changeFunc, increment) => {
    const newIndex = currentIndex + increment;
    if (newIndex >= 0 && newIndex < emailsLength) {
      changeFunc(newIndex);
    }
  };

  return (
    <div className="email-viewer-container">
      <div className="email-box human-sorted">
        <h2>Human Sorted Emails</h2>
        <Email email={humanSortedEmails[humanSortedIndex] ? humanSortedEmails[humanSortedIndex] : null} />
        <EmailControls
          changeIndex={changeIndex}
          currentIndex={humanSortedIndex}
          emailsLength={humanSortedEmails.length}
          buttonTexts={{ previous: 'Previous', next: 'Next' }}
          changeFunc={setHumanSortedIndex}
/>
      </div>
      <div className="email-box unsorted">
        <h2>
          Unsorted Emails{' '}
          {unsortedEmails[unsortedIndex] && unsortedFilenames[unsortedIndex]}
        </h2>
        <Email email={unsortedEmails[unsortedIndex] ? unsortedEmails[unsortedIndex] : null} />
        <div>
          <label htmlFor="rating">Rating (1-10): </label>
          <input
            id="rating"
            type="number"
            min="1"
            max="10"
            value={rating}
            onChange={(e) => setRating(e.target.value)}
          />
        </div>
        <div>
          <label htmlFor="classification">Classification: </label>
          <input
            id="classification"
            type="text"
            value={classification}
            onChange={(e) => setClassification(e.target.value)}
          />
        </div>
        <button
          onClick={() =>
            moveEmail(unsortedEmails[unsortedIndex], `unsorted\\${unsortedFilenames[unsortedIndex]}`)
          }
          disabled={!rating || !classification}
        >
          Submit and Move Email
        </button>
        <button
          onClick={() =>
            deleteEmail(unsortedEmails[unsortedIndex], `unsorted\\${unsortedFilenames[unsortedIndex]}`)
          }
        >
          Delete Email
        </button>
        <EmailControls
          changeIndex={changeIndex}
          currentIndex={unsortedIndex}
          emailsLength={unsortedEmails.length}
          buttonTexts={{ previous: 'Previous', next: 'Next' }}
          changeFunc={setUnsortedIndex}
/>
      </div>
    </div>
  );
};

export default EmailViewer;
