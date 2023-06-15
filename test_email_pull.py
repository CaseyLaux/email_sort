import imaplib, email
import base64, json, quopri
from secrats import decrypt_secrets, ColinGTK
from datetime import datetime, timedelta
from email.header import decode_header
import logging
import uuid
from pymongo import MongoClient
from secrats import decrypt_secrets, ColinGTK
from email.header import decode_header
import bot_sort
import re
import pytz
from bs4 import BeautifulSoup
# Setting up logging vars
breaker = "#" * 60
big_breaker = ("#" * 120) + "\n" + ("#" * 120)

# Setting up login creds for user
logging.info(f"EMAIL PULLER RUN {datetime.now()}")
logging.info(big_breaker)
logging.info("Fetching credentials")
logging.info(breaker)


def get_emails():
    user, secret = decrypt_secrets()
    email_address = user
    password = secret

    # Setting up vars for database
    mongo_uri = "mongodb://localhost:27017/"

    account_instance = ColinGTK()
    account_string = account_instance.Account_ID
    account_address = account_instance.user
    bot_sorted_collection_string = (str(account_address) + "_bot_sorted") 



    # Connecting to database
    client = MongoClient(mongo_uri)
    db = client[account_string]
    debug_db = client["debug"]

    # Setting up collections
    address_collection = db[account_address]
    bot_collection = db[bot_sorted_collection_string]
    debug_collection = debug_db["debug"]
    debug_string = str(uuid.uuid4())
    debug_collection.insert_one({"debug_string": debug_string})
    debug_filter = {"debug_string": debug_string}

    account_data = {
            "account_string": account_string,
            "account_address": account_address,
            "bot_sorted_collection_string": bot_sorted_collection_string,
            "email_id": "",
        }
    breaker = "#" * 60
    big_breaker = ("#" * 120) + "\n" + ("#" * 120)

    # Set up IMAP
    imap_server = 'imap.gmail.com'
    logging.info(big_breaker)
    logging.info(f"Connecting to {imap_server}")
    logging.info(breaker)
    
    
    imap = imaplib.IMAP4_SSL(imap_server)
    imap.login(email_address, password)
    start_datetime = datetime.now(pytz.utc) - timedelta(hours=120)
    end_datetime = datetime.now(pytz.utc) - timedelta(hours=60)

# format them as strings to use in the IMAP search
    start_date_str = start_datetime.strftime("%d-%b-%Y")
    end_date_str = end_datetime.strftime("%d-%b-%Y")

    imap.select('Inbox')
    logging.info(f"searching for emails since ")

    # pulling emails since since_date var hours ago
    def get_emails_since(con, since, before):
            result, data = con.search(None, 'SINCE', since, 'BEFORE', before)
            return data
    logging.info(breaker)
    logging.info("Fetching emails since {since_date}")

    # Using search results to pull emails since since_date
    search_results = get_emails_since(imap, start_date_str, end_date_str)
    def decode_content(part, i):
            
        # Pull charset and encoding to decode body text
        charset = part.get_content_charset()  # Get the charset
        encoding = part.get('Content-Transfer-Encoding')  # Get the encoding

        debug_encoding = str(encoding) + str(i)
        debug_charset = str(charset) + str(i)

        if charset is None:
            charset = 'utf-8'  # Use a default charset if none is specified
        
        payload = part.get_payload(decode=True)

        debug_payload = str(payload) + str(i)
        debug_encoded = str(part.get_payload())  + str(i)

        update_values = {"$set": {f"encoding {i}": debug_encoding, f"encoded {i}": debug_encoded, f"charset {i}": debug_charset, f"decoded {i}": debug_payload}}

        debug_collection.update_one(debug_filter, update_values)
        payload = payload.decode(charset, errors='replace')
        clean_body = payload.replace('  ', '').replace('\r', '').replace('\u200c', '').replace('\u0020', '')
        #if part.get('Content-Transfer-Encoding') == 'quoted-printable':
        if payload is None:
            payload =  ''
        if len(clean_body) > 1000:
            clean_body = clean_body[:1000]
        #clean_body = clean_body.decode(charset)
        return payload, clean_body 
    
    def decode_header_value(value, i):


        decoded_header = decode_header(value)
        header_parts = []
        
        for decoded_string, encoding in decoded_header:
            if isinstance(decoded_string, bytes):
                if encoding:
                    old_string = decoded_string
                    decoded_string = decoded_string.decode(encoding)
                    update_values = {"$set": {f"Heading_encoding {i}": encoding, f"Heading_encoded_string{i}": old_string, f"decoded_string{i}": decoded_string}}
                    debug_collection.update_one(debug_filter, update_values)

                else:
                    old_string = decoded_string
                    encoding = 'utf-8'
                    decoded_string = decoded_string.decode('utf-8')
                    update_values = {"$set": {f"encoding {i}": encoding, f"encoded_string {i}": old_string, f"decoded_string {i}": decoded_string}}

                    debug_collection.update_one(debug_filter, update_values)

            header_parts.append(decoded_string)
        return ''.join(header_parts)
    # Arrays to add to email_data then to database 


    senders = []
    subjects = []
    bodies = []
    clean_bodies = []
    dates = []
    test_array = []
    html_bodies = []
    i = 0
    # Parse through data from email pull
    for search_results in search_results[0].split():


        i += 1
        _, data = imap.fetch(search_results, '(RFC822)')
        email_message = email.message_from_bytes(data[0][1])
        breaker = "#" * 60
        senders.append(email_message.get('From'))
        subject = email_message.get('Subject')
        clean_subject = decode_header_value(subject, i)
        subjects.append(clean_subject)
        dates.append(email_message.get('Date'))

        
        
        
        d = open("debug_emails_pull.txt", 'w')
        clean_body_parts = []
        body_parts = []
        html_body_parts = []
        x = 0
        decoded = False
        for part in email_message.walk():
            if part.get_content_type() == 'text/plain':
                body, clean_body = decode_content(part, i)
                body_parts.append(body)
                # Add the cleaned body parts to clean_body_parts as well
                clean_body_parts.append(clean_body)
            elif part.get_content_type() == 'text/html':
                body, clean_body = decode_content(part, i)
                html_body_parts.append(body)
        
        html_body = ''.join(html_body_parts)
        body = ''.join(body_parts)
        clean_body = ''.join(clean_body_parts)
        if body == '':
            body = html_body
        if clean_body == '':
            clean_body = body
        if len(clean_body) > 1000:
            clean_body = clean_body[:1000]
        debug_collection.update_one(debug_filter, {"$set": {f"body_parts {i} {x}": body_parts, f"clean_body_parts {i} {x}": clean_body_parts}})

        bodies.append(body)
        clean_bodies.append(clean_body)
        html_bodies.append(html_body)
    i = 0
    for i in range(len(senders)):
        email_id = str(uuid.uuid4())
        email_data = {
            "prompt": f"Subject: {subjects[i]}\nFrom:{senders[i]}\nTo:support@ourcompany.com\nDate:{dates[i]}\nContent:{clean_bodies[i]}\n###\n\n",
            "completion": " ",
            "email_subject": subjects[i],
            "email_sender": senders[i],
            "email_date": dates[i],
            "email_id": email_id,
            "body": bodies[i],
            "html_body": html_bodies[i]
        }
        logging.info(breaker)
        logging.info("Inserting email data into database")

        account_data["email_id"] = email_id
        j_account_data = json.dumps(account_data)
        logging.info(breaker)
        logging.info(f"Inserting email data into databases")
        address_collection.insert_one(email_data)
        bot_collection.insert_one(email_data)
        logging.info(breaker)
        logging.info("Running bot sort")
        bot_sort.categorize_emails(j_account_data)
    # Inserting email data into database
    
    imap.close()
if __name__ == '__main__':
     get_emails()