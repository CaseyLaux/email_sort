import React from 'react';
import './EmailList.css';

const EmailList = ({ emails, setCurrentEmail }) => {
  console.log(emails)
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

  const getClassForEmailType = (type) => {
    switch (type) {
      case 'Business':
        return 'button-business';
      case 'Marketing':
        return 'button-marketing';
      case 'Events':
        return 'button-events';
      case 'Spam':
        return 'button-spam';
      case 'Delivery':
        return 'button-delivery';
      case 'Analytics':
        return 'button-analytics';
      case 'Invoice':
        return 'button-invoice';
      case 'Urgent':
        return 'button-urgent';
      default:
        return '';
    }
  };

  const isPrime = (num) => {
    for (let i = 2, sqrt = Math.sqrt(num); i <= sqrt; i++) 
      if (num % i === 0) return false;
    return num > 1;
  };

  const formatDate = (unixTimestamp) => {
    const date = new Date(unixTimestamp * 1000);
    return date.toLocaleString();
  };
  const truncateText = (text, length = 100) => {
    return text.length > length ? text.slice(0, length) + "..." : text;
  };
  return (
    <div>
      {emails.map((email, index) => {
        let classification;
        let rating;
        const emailCompletionNumber = parseInt(email.completion, 10);

        for (let classKey in classificationValues) {
          let prime = classificationValues[classKey];
          if (emailCompletionNumber % prime === 0) {  // check divisibility first
            let possibleRating = emailCompletionNumber / prime;
            if (isPrime(possibleRating)) {
              classification = classKey;
              rating = Object.keys(rating_values).find(key => rating_values[key] === possibleRating);
              break;
            }
          }
        }

        return (
          <button
  key={index}
  className={`button ${getClassForEmailType(classification)}`} // use CSS class for background color
  onClick={() => setCurrentEmail(email)}
>
  
  <div>{truncateText(email.email_sender)}</div>
  <div>{truncateText(email.email_subject)}</div>
  <div className="date-time">{formatDate(email.email_unix_time)}</div>
  <span className="rating">{rating}</span>
</button>
        );
      })}
    </div>
  );
};

export default EmailList;
