// Importing necessary dependencies and components
import EmailDetail from './EmailDetail';
import React, { useState, useEffect } from 'react';
import './EmailViewer.css';
import Email from './Email';
import EmailControls from './EmailControls';
import EmailList from './EmailList';

// Defining a mapping for classification values and rating values
const CLASSIFICATION_VALUES = {
  Spam: 29,
  Marketing: 31,
  Events: 37,
  Delivery: 41,
  Analytics: 43,
  Business: 47,
  Invoice: 53,
  Urgent: 59,
};

const RATING_VALUES = {
  1: 2,
  2: 3,
  3: 5,
  4: 7,
  5: 11,
  6: 13,
  7: 17,
  8: 19,
  9: 23,
};

// Function to refresh emails
const refreshEmails = async () => {
  try {
    const response = await fetch('http://localhost:3001/api/refresh-emails');

    if (!response.ok) {
      throw new Error('Failed to refresh emails.');
    }

    alert('Emails refreshed successfully.');
  } catch (error) {
    alert('Failed to refresh emails.');
  }
};


// The main functional component
const EmailViewer = () => {
  // States for the component
  const [currentEmail, setCurrentEmail] = useState(null);
  const [humanSortedEmails, setHumanSortedEmails] = useState([]);
  const [userUnsortedEmails, setUserUnsortedEmails] = useState([]);
  const [humanSortedIndex, setHumanSortedIndex] = useState(0);
  const [unsortedIndex, setUnsortedIndex] = useState(0);
  const [rating, setRating] = useState('');
  const [classification, setClassification] = useState('');
  const [botSortedEmails, setBotSortedEmails] = useState([]);
  const [botSortedIndex, setBotSortedIndex] = useState(0);
  const [emailDetailViewOpen, setEmailDetailViewOpen] = useState(false);
  const [currentDetailViewEmail, setCurrentDetailViewEmail] = useState(null);

  // Functions for opening and closing the email detail view
  const openEmailDetailView = (email) => {
    // Find the index of the selected email
    const index = userUnsortedEmails.findIndex((e) => e._id === email._id);
    
    // Set the unsortedIndex to the selected email's index
    if (index !== -1) setUnsortedIndex(index);
    
    setCurrentEmail(email);
    setCurrentDetailViewEmail(email);
    setEmailDetailViewOpen(true);
  };

  const closeEmailDetailView = () => {
    setEmailDetailViewOpen(false);
  };

  // Function for deleting an email
  const deleteEmail = async (email) => {
    const email_id = {
      ...email,
      _id: email._id.$oid,
    };

    // Deleting an email from the API and updating state
    try {
      const response = await fetch('http://localhost:3001/api/delete-email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: email_id }),
      });

      if (!response.ok) {
        throw new Error('Failed to delete email.');
      }

      setUserUnsortedEmails((prevState) => prevState.filter((e) => e._id !== email._id));
  
      alert('Email deleted successfully.');
    } catch (error) {
      alert('Failed to delete email.');
    }
  };

  // Function for loading emails on component mount
  useEffect(() => {
    async function loadEmails() {
      try {
        const response = await fetch('http://localhost:3001/api/get-emails');
        const data = await response.json();

        setHumanSortedEmails(data.user_sorted_emails);
        setUserUnsortedEmails(data.user_unsorted_emails);
        setBotSortedEmails(data.bot_sorted_emails);
        
      } catch (error) {
        console.error('Error loading emails:', error);
      }
    }

    loadEmails();
  }, []);

  // Function for updating an email
  const updateEmail = async (email) => {
    // Validation for rating and classification inputs
    if (!rating || !classification) {
      alert('Please enter a rating and classification.');
      return;
    }
    
    const classificationValue = CLASSIFICATION_VALUES[classification];
    if (!classificationValue) {
      alert('Invalid classification.');
      return;
    }

    const ratingValue = RATING_VALUES[rating];
    if (!ratingValue) {
      alert('Invalid Rating.');
      return;
    }

    // Create updated email
    let completionValue = ratingValue * classificationValue;
    const updatedEmail = {
      ...email,
      completion: completionValue,
      _id: email._id.$oid,
    };
  
    // Move email by updating on the server
    try {
      const response = await fetch('http://localhost:3001/api/move-email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: updatedEmail }),
      });

      if (!response.ok) {
        throw new Error('Failed to move email.');
      }
  
      setUserUnsortedEmails((prevState) => prevState.filter((e) => e._id !== email._id));
  
      // Reset rating and classification inputs
      setRating('');
      setClassification('');
  
      alert('Email moved successfully.');
    } catch (error) {
      alert('Failed to move email.');
    }
  };
  
  const changeIndex = (currentIndex, emailsLength, changeFunc, increment) => {
    const newIndex = currentIndex + increment;
    if (newIndex >= 0 && newIndex < emailsLength) {
      changeFunc(newIndex);
    }
  };

  // Component render
  return (
    <div className="email-viewer-container">
      <div className="email-unsorted-list" >
      <button onClick={refreshEmails}>Refresh Emails</button>
        <h3>Unsorted emails</h3>
        <EmailList emails={userUnsortedEmails} setCurrentEmail={openEmailDetailView} />
      </div>
      <div className="email-box unsorted">
        <h2>
          Selected email
        </h2>
        <Email email={currentEmail} />
        <div>
          <label htmlFor="Rating">Rating: </label>
          <select
            id="Rating"
            value={rating}
            onChange={(e) => setRating(e.target.value)}
          >
            <option value="">Select a Rating</option>
            {Object.keys(RATING_VALUES).map((key) => (
              <option key={key} value={key}>
                {key}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label htmlFor="classification">Classification: </label>
          <select
            id="classification"
            value={classification}
            onChange={(e) => setClassification(e.target.value)}
          >
            <option value="">Select a classification</option>
            {Object.keys(CLASSIFICATION_VALUES).map((key) => (
              <option key={key} value={key}>
                {key}
              </option>
            ))}
          </select>
        </div>
        <button
          onClick={() =>
            updateEmail(userUnsortedEmails[unsortedIndex])
          }
          disabled={!rating || !classification}
        >
          Submit and Move Email
        </button>
        <button
          onClick={() =>
            deleteEmail(userUnsortedEmails[unsortedIndex])
          }
        >
          Delete Email
        </button>
        <EmailControls
          changeIndex={changeIndex}
          currentIndex={unsortedIndex}
          emailsLength={userUnsortedEmails.length}
          buttonTexts={{ previous: 'Previous', next: 'Next' }}
          changeFunc={setUnsortedIndex}
        />
      </div>
      <div className="email-unsorted-list" >
        <h2>Sorted emails</h2>
        <h4>Human Sorted</h4>
        <EmailList emails={humanSortedEmails} setCurrentEmail={openEmailDetailView} />
          <h2>Bot Sorted</h2>
        <EmailList emails={botSortedEmails} setCurrentEmail={openEmailDetailView} />
      </div>
    </div>
  );
  
  // End of the component
  };
  export default EmailViewer;
