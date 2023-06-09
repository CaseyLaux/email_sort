const EmailList = ({ emails, setCurrentEmail }) => {
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

  const colorValues = {
    Business: 'blue',
    Marketing: 'green',
    Events: 'orange',
    Spam: 'white',
    Delivery: 'yellow',
    Analytics: 'grey',
    Invoice: 'red',
    Urgent: 'brightred',
  };

  const isPrime = (num) => {
    for (let i = 2, sqrt = Math.sqrt(num); i <= sqrt; i++) 
      if (num % i === 0) return false;
    return num > 1;
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
            style={{ backgroundColor: colorValues[classification] || 'default' }} // default is the color if classification does not exist in colorValues
            onClick={() => setCurrentEmail(email)}
          >
            {email.email_sender} - {email.email_subject} - Classification: {classification} - Rating: {rating}
          </button>
        );
      })}
    </div>
  );
};

export default EmailList;
