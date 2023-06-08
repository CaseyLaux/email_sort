import React from 'react';

const EmailList = ({ emails, setCurrentEmail }) => {
  return (
    <div>
      {emails.map((email, index) => {
        let classification;
        let rating;
        const emailCompletionNumber = parseInt(email.completion, 10);

        for (let classKey in classificationValues) {
          let prime = classificationValues[classKey];
          let possibleRating = emailCompletionNumber / prime;
          if (isPrime(possibleRating)) {
            classification = classKey;
            rating = Object.keys(rating_values).find(key => rating_values[key] === possibleRating);
            break;
          }
        }
        switch (parseInt(email.completion, 10)) {
          case 611:
              buttonColor = 'red';
              buttonText = `Important - Rating ${email.completion}`;
              break;
          case 93:
              buttonColor = 'green';
              buttonText = `Normal - Rating ${email.completion}`;
              break;
          default:
              buttonColor = 'blue'; // default color
              buttonText = `No Classification - Rating ${email.completion}`;
      }

        return (
          <button
            key={index}
            style={{backgroundColor: buttonColor}}
            onClick={() => setCurrentEmail(email)}
          >
            {email.email_sender} - {email.email_subject} - {buttonText}
          </button>
        );
      })}
    </div>
  );
};

export default EmailList;
