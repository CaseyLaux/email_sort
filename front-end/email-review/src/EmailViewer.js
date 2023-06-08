import EmailDetail from './EmailDetail';
import React, { useState, useEffect } from 'react';
import './EmailViewer.css';
import Email from './Email';
import EmailControls from './EmailControls';
import EmailList from './EmailList';

const EmailViewer = () => {
  const [currentEmail, setCurrentEmail] = useState(null);
  const classificationValues = {
    Spam: 29,
    Marketing: 31,
    Events: 37,
    Delivery: 41,
    Analytics: 43,
    Business: 47,
    Invoice: 53,
    Urgent: 59,
  };
  const rating_values = {
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
  const [humanSortedEmails, setHumanSortedEmails] = useState([]);
  const [user_unsorted_Emails, setUserUnsortedEmails] = useState([]);
  const [humanSortedIndex, setHumanSortedIndex] = useState(0);
  const [unsortedIndex, setUnsortedIndex] = useState(0);
  const [rating, setRating] = useState('');
  const [classification, setClassification] = useState('');
  
  const [emailDetailViewOpen, setEmailDetailViewOpen] = useState(false);
  const [currentDetailViewEmail, setCurrentDetailViewEmail] = useState(null);

  
  const openEmailDetailView = (email) => {
    console.log('Opening email detail view for email:', email);
    setCurrentEmail(email);
    setCurrentDetailViewEmail(email);
    setEmailDetailViewOpen(true);
  };

  const closeEmailDetailView = () => {
    setEmailDetailViewOpen(false);
  };

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
      setUserUnsortedEmails((prevState) => prevState.filter((e) => e._id !== email._id));
  
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
        setHumanSortedEmails(data.user_sorted_emails);
        setUserUnsortedEmails(data.user_unsorted_emails);
      } catch (error) {
        console.error('Error loading emails:', error);
      }
    }

    loadEmails();
  }, []);

  const update_email = async (email) => {
    // Validate rating and classification inputs
      if (!rating || !classification) {
        alert('Please enter a rating and classification.');
        return;
      }
    
      // Get classification value
      const classificationValue = classificationValues[classification];
      if (!classificationValue) {
        alert('Invalid classification.');
        return;
      }
      const ratingValue = rating_values[rating];
      if (!rating) {
        alert('Invalid Rating.');
      return;
    }
    let completionValue = ratingValue * classificationValue;
    // Add classification value and rating to the email completion field
    const updatedEmail = {
      ...email,
      completion: completionValue,
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
      setUserUnsortedEmails((prevState) => prevState.filter((e) => e._id !== email._id));
  
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
  <div className="email-unsorted-list" >
    <h3>Unsorted emails</h3>
    <EmailList emails={user_unsorted_Emails} setCurrentEmail={openEmailDetailView} />
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
        {Object.keys(rating_values).map((key) => (
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
        {Object.keys(classificationValues).map((key) => (
          <option key={key} value={key}>
            {key}
          </option>
        ))}
      </select>
    </div>
    <button
      onClick={() =>
        update_email(user_unsorted_Emails[unsortedIndex])
      }
      disabled={!rating || !classification}
    >
      Submit and Move Email
    </button>
    <button
      onClick={() =>
        deleteEmail(user_unsorted_Emails[unsortedIndex])
      }
    >
      Delete Email
    </button>
    <EmailControls
      changeIndex={changeIndex}
      currentIndex={unsortedIndex}
      emailsLength={user_unsorted_Emails.length}
      buttonTexts={{ previous: 'Previous', next: 'Next' }}
      changeFunc={setUnsortedIndex}
    />
  </div>
  <div className="email-unsorted-list" >
    <h3>Sorterd emails</h3>
    <EmailList emails={humanSortedEmails} setCurrentEmail={openEmailDetailView} />
  </div>
</div>

  );
};

export default EmailViewer;
