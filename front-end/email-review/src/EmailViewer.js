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

  useEffect(() => {
    async function loadHumanSortedEmails() {
      try {
        const humanSortedUrl = `${process.env.PUBLIC_URL}/human_sorted/index.json`;
        console.log('Fetching human_sorted index:', humanSortedUrl);
        const humanSortedResponse = await fetch(humanSortedUrl);
        const humanSortedFilenames = await humanSortedResponse.json();

        const humanSortedEmailPromises = humanSortedFilenames.map(async (filename) => {
          const emailResponse = await fetch(`${process.env.PUBLIC_URL}/human_sorted/${filename}`);
          return await emailResponse.json();
        });

        const loadedHumanSortedEmails = await Promise.all(humanSortedEmailPromises);
        return loadedHumanSortedEmails;
      } catch (error) {
        console.error('Error loading human_sorted emails:', error);
      }
    }

    async function loadUnsortedEmails() {
      try {
        const unsortedUrl = `${process.env.PUBLIC_URL}/unsorted/index.json`;
        console.log('Fetching unsorted index:', unsortedUrl);
        const unsortedResponse = await fetch(unsortedUrl);
        const unsortedFilenames = await unsortedResponse.json();

        const start = 0;
        const limit = 50;
        const end = Math.min(start + limit, unsortedFilenames.length);

        const unsortedEmailPromises = unsortedFilenames.slice(start, end).map(async (filename) => {
          const emailResponse = await fetch(`${process.env.PUBLIC_URL}/unsorted/${filename}`);
          return await emailResponse.json();
        });

        const loadedUnsortedEmails = await Promise.all(unsortedEmailPromises);
        return { unsorted: loadedUnsortedEmails, filenames: unsortedFilenames };
      } catch (error) {
        console.error('Error loading unsorted emails:', error);
      }
    }

    loadHumanSortedEmails().then(setHumanSortedEmails);
    loadUnsortedEmails().then((loadedUnsortedEmails) => {
      setUnsortedEmails(loadedUnsortedEmails.unsorted);
      setUnsortedFilenames(loadedUnsortedEmails.filenames);
    });
  }, []);

  const moveEmail = async (email, originalPath) => {
    // Validate rating and classification inputs
    if (!rating || !classification) {
      alert('Please enter a rating and classification.');
      return;
    }

    const newPath = `human_sorted\\${classification}_${rating}_${email.email_date.replace(/[^a-zA-Z0-9]/g, '_')}_${email.email_sender.replace(/[^a-zA-Z0-9]/g, '_')}.json`;
    // Log the filename before saving it
    console.log('Saving email to:', newPath);
    try {
      const response = await fetch('http://localhost:3001/api/move-email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ originalPath, newPath }),
      });

      if (!response.ok) {
        throw new Error('Failed to move email.');
      }

      // Update unsortedEmails state to remove the moved email
      setUnsortedEmails((prevState) => prevState.filter((e) => e !== email));

      // Reset rating and classification inputs
      setRating('');
      setClassification('');

      alert('Email moved successfully.');
      async function callPythonScript() {
    const url = "http://localhost:5000/index_emails";
    const data = {
      
    };
  
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });
  
      if (response.ok) {
        const result = await response.json();
        console.log('Python script result:', result);
      } else {
        console.error('Error calling Python script:', response.status, response.statusText);
      }
    } catch (error) {
      console.error('Error calling Python script:', error);
    }
  }
  
  // Call the function without blocking the main process
  callPythonScript();
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
        <Email email={humanSortedEmails[humanSortedIndex]} />
        <EmailControls
          changeIndex={changeIndex}
          currentIndex={humanSortedIndex}
          emailsLength={humanSortedEmails.length}
          buttonTexts={{ previous: 'Previous', next: 'Next' }}
        />
      </div>
      <div className="email-box unsorted">
        <h2>
          Unsorted Emails{' '}
          {unsortedEmails[unsortedIndex] && unsortedFilenames[unsortedIndex]}
        </h2>
        <Email email={unsortedEmails[unsortedIndex]} />
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
        <EmailControls
          changeIndex={changeIndex}
          currentIndex={unsortedIndex}
          emailsLength={unsortedEmails.length}
          buttonTexts={{ previous: 'Previous', next: 'Next' }}
        />
      </div>
    </div>
  );
};

export default EmailViewer;
