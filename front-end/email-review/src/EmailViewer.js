// Importing necessary dependencies and components
import { Link } from 'react-router-dom';
import { FaUserCircle } from 'react-icons/fa';
import EmailDetail from './EmailDetail';
import React, { useState, useEffect } from 'react';
import './EmailViewer.css';
import EmailList from './EmailList';
import Profile from './profile';
import { FaRegTrashAlt, FaArrowRight, FaArrowLeft, FaEnvelopeOpenText, FaRedo } from 'react-icons/fa';
// Defining a mapping for classification values and rating values
const COLOR_VALUES = {
  Spam: '#000000',
  Marketing: '#28a745',
  Events: '#ffc107',
  Delivery: 'cyan',
  Analytics: 'grey',
  Business: 'blue',
  Invoice: '#20c997',
  Urgent: 'red',
};
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
  const token = localStorage.getItem('jwt');
  try {
    const response = await fetch('http://localhost:3001/api/refresh-emails', {
      method: 'GET', // or 'POST'
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    });

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
  const [selectedType, setSelectedType] = useState('');
  const [currentCategory, setCurrentCategory] = useState('Bot Sorted');
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
  const [isLoading, setIsLoading] = useState(false);
  const categories = ['spam', 'marketing', 'events', 'delivery', 'analytics', 'business', 'invoice', 'urgent'];
  const [username, setUsername] = useState(null);
  const [error, setError] = useState(null);

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
  const getFilteredEmails = () => {
    const allEmails = getCurrentEmails();
    return selectedType ? allEmails.filter(email => email.type === selectedType) : allEmails;
  };
  
  
  
  // Function for deleting an email
  
  const deleteEmail = async () => {
    const email_id = {
      ...currentDetailViewEmail,
      _id: currentDetailViewEmail._id.$oid,
    };
  
    try {
      // Get JWT token from local storage
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No token found in local storage.');
      }
  
      // Send token to the authentication server and get the username
      let usernameResponse = await fetch('http://localhost:3001/api/v1/auth-check', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
      });
  
      if (!usernameResponse.ok) {
        throw new Error('Failed to get username from auth server.');
      }
  
      let { username } = await usernameResponse.json();
  
      // Delete the email using the fetched username
      const response = await fetch(`http://localhost:3001/api/${username}/delete-email`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: email_id }),
      });
  
      if (!response.ok) {
        throw new Error('Failed to delete email.');
      }
  
      setUserUnsortedEmails((prevState) => prevState.filter((e) => e._id !== currentDetailViewEmail._id));
  
      alert('Email deleted successfully.');
    } catch (error) {
      alert(`Failed to delete email. Error: ${error.message}`);
    }
  };
  
  const groupEmailsByCompletion = (emails) => {
    console.log(emails)
    // Create an empty object to hold the groups
    let emailGroups = {};
  
    // Loop over the emails
    emails.forEach(email => {
      // Check if the email category is in the list of categories
      if (categories.includes(email.category)) {
        // If the category group doesn't exist yet, create it
        if (!emailGroups[email.category]) {
          emailGroups[email.category] = [];
        }
    
        // Add the email to the category group
        emailGroups[email.category].push(email);
      }
    });
    
    return emailGroups;
  };
  // Function for loading emails on component mount
  useEffect(() => {
    async function checkAuthAndGetUsername() {
      try {
        // Get JWT token from local storage
        const token = localStorage.getItem('jwt');
        if (!token) {
          throw new Error('No token found in local storage.');
        }
  
        // Send token to the authentication server and get the username
        let response = await fetch('http://localhost:8081/api/v1/auth-check', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
        });
  
        if (!response.ok) {
          throw new Error('Failed to get username from auth server.');
        }
  
        let data = await response.json();
        setUsername(data.username);
        console.log(data.username)
        // setUsername(data.username);
      } catch (error) {
        console.error('Error fetching username:', error);
      }
    }
  
    // Call the async function
    checkAuthAndGetUsername();
    async function loadEmails() {
      try {
        const token = localStorage.getItem('jwt');  
      const response = await fetch('http://localhost:3001/api/get-emails', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      const data = await response.json();

        // console.log(data)
        setHumanSortedEmails(data.user_sorted_emails);
        setUserUnsortedEmails(data.user_unsorted_emails);
        setBotSortedEmails(data.bot_sorted_emails);
        const groupedEmails = groupEmailsByCompletion(data.bot_sorted_emails);

        //setLoading(false)
      } catch (error) {
        console.error('Error loading emails:', error);
      }
    }

    setIsLoading(true);
    loadEmails()
      .then((data) => {
        setHumanSortedEmails(data.user_sorted_emails);
        setUserUnsortedEmails(data.user_unsorted_emails);
        setBotSortedEmails(data.bot_sorted_emails);
        setIsLoading(false);
      })
      .catch((error) => {
        console.error('Error loading emails:', error);
        setError('Error loading emails.');
        setIsLoading(false);
      });
  }, []);




  // Function for updating an email
  const updateEmail = async () => {
    const token = localStorage.getItem('jwt');
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
      ...currentDetailViewEmail,
      completion: completionValue,
      _id: currentDetailViewEmail._id.$oid,
    };
  
    // Move email by updating on the server
    try {
      console.log({email: updatedEmail})
      const response = await fetch('http://localhost:3001/api/move-email', {
      method: 'POST',
      
        headers: { 
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
      },
        body: JSON.stringify({ email: updatedEmail }),
      });
      //await refreshEmails();
      // window.location.reload();
      if (!response.ok) {
        throw new Error('Failed to move email.');
      }
  
      setUserUnsortedEmails((prevState) => prevState.filter((e) => e._id !== currentDetailViewEmail._id));
      
  
      // Reset rating and classification inputs
      setRating('');
      setClassification('');
  
      alert('Email moved successfully.');
    } catch (error) {
      alert('Failed to move email.');
    }
  };
  const resortEmails = async () => {
    try {
      const token = localStorage.getItem('jwt'); // get the token from the storage
    
      const response = await fetch('http://localhost:3001/api/resort-emails', {
        method: 'GET', // or 'POST'
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}` // attach the token as a Bearer token
        }
      });
    
      if (!response.ok) {
        throw new Error('Failed to resort emails.');
      }
    
      alert('Emails resorted successfully.');
    } catch (error) {
      alert('Failed to resort emails.');
    }
    
  };
  const getCurrentEmails = () => {
    switch (currentCategory) {
      case 'Unsorted':
        return userUnsortedEmails;
      case 'Human Sorted':
        return humanSortedEmails;
      case 'Bot Sorted':
        return botSortedEmails;
      case 'spam':
      case 'marketing':
      case 'events':
      case 'delivery':
      case 'analytics':
      case 'business':
      case 'invoice':
      case 'urgent':
      case 'rating_error':
        // If the current category is any of these, return emails from all lists that match the category
        return [...userUnsortedEmails, ...humanSortedEmails, ...botSortedEmails].filter(email => 
          email && 
          email.category && 
          email.category.toLowerCase() === currentCategory.toLowerCase()
        );
      default:
        return [];
    }
  };
  // Component render
  return (
    <div className="email-viewer-container" style={{display: 'flex'}}>
  {isLoading ? <p>Loading...</p> : null}
  <div className="email-sidebar" style={{width: '300px'}}>
  <h3>Siemless emails</h3>
  <button onClick={resortEmails}>
  <FaRedo /> 
</button>
<button onClick={refreshEmails}>
      <FaEnvelopeOpenText /> resort
    </button>
    
    
    <ul>
      <li onClick={() => setCurrentCategory('Human Sorted')}>Human Sorted</li>
      <li onClick={() => setCurrentCategory('Bot Sorted')}>Emails</li>
      <div className="color-key">
      <h3>Categories</h3>
      <ul>
      {Object.keys(COLOR_VALUES).map((key) => (
  <li key={key} style={{color: COLOR_VALUES[key]}} onClick={() => setCurrentCategory(key.toLowerCase())}>
    {key}
  </li>
))}
    </ul>
    </div>
    </ul>
    <Link to="/profile" className="profile-icon">
    <FaUserCircle size={30} />
  </Link>
  </div>
  <div className="email-main-content" style={{flexGrow: 1}}>
    {emailDetailViewOpen ? (
      <>
        <h2>Selected Email</h2>
        <EmailDetail email={currentDetailViewEmail} onClose={closeEmailDetailView} />
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
        <div className="email-action-buttons">
          <button
            onClick={() => updateEmail(getCurrentEmails()[unsortedIndex])}
            disabled={!rating || !classification}
          >
            Submit and Move Email
          </button>
          <button
            onClick={() => deleteEmail(getCurrentEmails()[unsortedIndex])}
          >
            <FaRegTrashAlt /> Delete Email
          </button>
        </div>
      </>
    ) : (
      <>
        <h3>{currentCategory} Emails</h3>
        <EmailList emails={getCurrentEmails()} setCurrentEmail={openEmailDetailView} />
      </>
    )}
  </div>
</div>
);
  
  // End of the component
  };
  export default EmailViewer;
