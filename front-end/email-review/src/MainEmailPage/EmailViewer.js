import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { FaUserCircle, FaRegTrashAlt, FaEnvelopeOpenText, FaRedo } from 'react-icons/fa';
import EmailDetail from './EmailDetail';
import EmailList from './EmailList';
import './EmailViewer.css';

//const subdomains = {
//  email_server: "https://serve.siemlessemail.com",
//  auth_server: "https://auth.siemlessemail.com",
//  front_end: "https://email.siemlessemail.com"
//}
const subdomains = {
  email_server: "http://127.0.0.1:3001",
  auth_server: "http://127.0.0.1:8081",
  front_end: "http://127.0.0.1:3000"
}



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
const categories = ['spam', 'marketing', 'events', 'delivery', 'analytics', 'business', 'invoice', 'urgent'];


// This function grabs the jwt token from storage and sends it to the refresh emails endpoint
const refreshEmails = async () => {
  const token = localStorage.getItem('jwt');
  let refresh_url = `${subdomains.email_server}/api/refresh-emails`;
  try {
    const response = await fetch(refresh_url, {
      method: 'GET', 
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
  const [emailsByAccount, setEmailsByAccount] = useState({});
  const [emailAccountNames, setEmailAccountNames] = useState([]);
  const [currentEmail, setCurrentEmail] = useState(null);
  const [currentCategory, setCurrentCategory] = useState('');
  const [humanSortedEmails, setHumanSortedEmails] = useState([]);
  const [userUnsortedEmails, setUserUnsortedEmails] = useState([]);
  const [unsortedIndex, setUnsortedIndex] = useState(0);
  const [rating, setRating] = useState('');
  const [classification, setClassification] = useState('');
  const [botSortedEmails, setBotSortedEmails] = useState([]);
  const [emailDetailViewOpen, setEmailDetailViewOpen] = useState(false);
  const [currentDetailViewEmail, setCurrentDetailViewEmail] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [currentEmailAccount, setCurrentEmailAccount] = useState(null);
  

  // This function checks the current email and opens it in the emailDetailView
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
      let AuthCheckUrl = `${subdomains.auth_server}/api/v1/auth-check`;
      let usernameResponse = await fetch(AuthCheckUrl, {
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
      let delete_url = `${subdomains.email_server}/api/${username}/delete-email`

      const response = await fetch(delete_url, {
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

  // This function looks at the emails during the import and adds them to their respective category
  const groupEmailsByCompletion = (emails) => {
    let emailGroups = {};
  
    emails.forEach(email => {
      if (categories.includes(email.category)) {
        if (!emailGroups[email.category]) {
          emailGroups[email.category] = [];
        }
    
        emailGroups[email.category].push(email);
      }
    });
    
    return emailGroups;
  };


  // Function for loading emails on component mount
  useEffect(() => {
    
    

     // This function sends the jwt token to the get-emails endpoint and recieves the emails
     async function loadEmails() {
      try {
        const token = localStorage.getItem('jwt');
        let load_url = `${subdomains.email_server}/api/get-emails`;
        const response = await fetch(load_url, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        const data = await response.json();
    
        let emailsByAccount = {};
        let emailAccountNames = [];
        let allEmails = []; 
    
        for (const emailAccount in data) {
          emailsByAccount[emailAccount] = data[emailAccount];
          emailAccountNames.push(emailAccount); // Add the email account name to the list
          allEmails = allEmails.concat(data[emailAccount]);
        }
        
        setEmailsByAccount(emailsByAccount);
        setEmailAccountNames(emailAccountNames); 
        emailsByAccount["All emails"] = allEmails;
        console.log(emailsByAccount["All emails"])
        setIsLoading(false)

      } catch (error) {
        console.error("An error occurred while loading emails:", error);
      }
    }

    setIsLoading(true);
    loadEmails()
      .catch((error) => {
        console.error('Error loading emails:', error);
        setError('Error loading emails.');
        setIsLoading(false);
      });
  }, []);




  // This function passes the jwt token and current email then sends them to the move-email endpoint
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

    
    let completionValue = ratingValue * classificationValue;
    const updatedEmail = {
      ...currentDetailViewEmail,
      completion: completionValue,
      _id: currentDetailViewEmail._id.$oid,
    };
  

    try {
      console.log({email: updatedEmail})
      let move_url = `${subdomains.email_server}/api/move-email`;
      const response = await fetch(move_url, {
      method: 'POST',
      
        headers: { 
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
      },
        body: JSON.stringify({ email: updatedEmail }),
      });
      
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


  // This function sends the jwt token to the resort-emails endpoint 
  const resortEmails = async () => {
    try {
      const token = localStorage.getItem('jwt');

      let resort_url = `${subdomains.email_server}/api/resort-emails`;
      const response = await fetch(resort_url, {
        method: 'GET', // or 'POST'
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}` 
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
    console.log('Current Category:', currentCategory);
  
    const nonAccountCategories = [
      'spam', 'marketing', 'events', 
      'delivery', 'analytics', 'business', 
      'invoice', 'urgent', 'rating_error'
    ];
    
    const allEmailSources = [
      ...userUnsortedEmails,
      ...humanSortedEmails,
      ...botSortedEmails,
      ...emailsByAccount["All emails"]
    ];
    
    if (nonAccountCategories.includes(currentCategory.toLowerCase())) {
      return allEmailSources.filter(email => 
        email && 
        email.category && 
        email.category.toLowerCase() === currentCategory.toLowerCase()
      );
    }
  
    if (currentCategory === 'All Emails') {
      return emailsByAccount["All emails"];
    }
  
    if (emailsByAccount[currentCategory]) {
      return emailsByAccount[currentCategory];
    }
  
    return [];
  };


  // Component render
  return (
    <div className="email-viewer-container" style={{display: 'flex'}}>
  {isLoading ? <p>Loading...</p> : null}

  {/* email sidebar */}
  <div className="email-sidebar" style={{width: '300px'}}>
  <h3>Siemless emails</h3>
  <button onClick={resortEmails}>
  <FaRedo /> 
</button>
<button onClick={refreshEmails}>
      <FaEnvelopeOpenText /> 
    </button>
    
    <ul>
    <li onClick={() => setCurrentCategory('All Emails')}>All Emails</li>
        {emailAccountNames.map((emailAccountName, index) => (
          <li key={index} onClick={() => setCurrentCategory(emailAccountName)}>
            {emailAccountName}
          </li>
        ))}
      </ul>
    <ul>
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

  {/* Main content */}
  <div className="email-main-content" style={{flexGrow: 1}}>
    {emailDetailViewOpen ? (
      <>
        <h2>Selected Email</h2>
        <EmailDetail email={currentDetailViewEmail} onClose={closeEmailDetailView} />

              {/* Rating and Classification inputs */}
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

              {/* Submit and Delete buttons */}
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
        <h3>{currentCategory}</h3>
        <EmailList emails={getCurrentEmails()} setCurrentEmail={openEmailDetailView} />
      </>
    )}


  </div>
</div>
);
  
  };
  export default EmailViewer;
