import imaplib, email
import base64, json, quopri
from datetime import datetime, timedelta
from email.header import decode_header
import logging
import uuid
from pymongo import MongoClient
from email.header import decode_header
import bot_sort
import pytz

# Setting up logging vars


# Setting up login creds for user

def extract_user_data(mongoDB):
    user_data = {}  # This dictionary will store all the data

    userListDB = mongoDB['ai']
    userListDocs = userListDB['users'].find({})

    for userDoc in userListDocs:
        username = userDoc['username']
        print(f"Found user {username}")

        # Initialize a dictionary for the user
        user_data[username] = {
            "email_accounts": []
        }

        userDB = mongoDB[username]
        emailAccountDocs = userDB['email_accounts'].find({})

        for emailAccountDoc in emailAccountDocs:
            email_address = emailAccountDoc['email']
            print(f"found email {email_address}")
            emailSecret = emailAccountDoc['secret']

            # Create a dictionary for the email account data
            email_account_data = {
                "email_address": email_address,
                "secret": emailSecret,
                "emails": []  # This list will store the emails for the email account, if any
            }

            emailDocs = userDB[email_address]
            # If you want to fetch the actual email documents for the account, you can iterate through emailDocs and append them to email_account_data["emails"]

            botSortString_S = email_address + "_bot_sort"
            bot_sorted_collection = userDB[botSortString_S]

            emailAccountDataDoc = userDB["email_accounts"].find_one({'email': str(email_address)})
            
            try:
                last_timestamp_doc = emailAccountDataDoc["timestamp"]
            except KeyError:
                last_timestamp_doc = None

            email_account_data["last_timestamp"] = last_timestamp_doc

            user_data[username]["email_accounts"].append(email_account_data)

    return user_data
def get_emails():

    if last_timestamp_doc is None:
                # if it's the first time, default to 120 hours ago
                start_datetime = datetime.now(pytz.utc) - timedelta(hours=120)

    # Setting up vars for database
    mongo_uri = "mongodb://localhost:27017/"
    client = MongoClient(mongo_uri)

    debug_db = client["debug"]
    debug_collection = debug_db["pull_emails"]
    debug_string = str(uuid.uuid4())
    debug_collection.insert_one({"debug_string": debug_string})
    debug_filter = {"debug_string": debug_string}

    users_db = client['ai']
    users = users_db['users'].find({})
    for user in users:
        username = user['username']
        print(f"Found user {username}")
        user_db = client[username]
        email_accounts = user_db['email_accounts'].find({}) 
        for email_account in email_accounts:
            email_address = email_account['email']
            print(f"found email {email_address}")
            email_secret = email_account['secret']
            email_collection = user_db[email_address]
            bot_sort_string = email_address + "_bot_sort"
            bot_sorted_collection = user_db[bot_sort_string]
            email_document = user_db["email_accounts"].find_one({'email': str(email_address)})
            try:
                last_timestamp_doc = email_document["timestamp"]
            except KeyError:
                last_timestamp_doc = None
            
            if last_timestamp_doc is None:
                # if it's the first time, default to 120 hours ago
                start_datetime = datetime.now(pytz.utc) - timedelta(hours=120)
                # create document
                update = {'timestamp': start_datetime}
                user_db["email_accounts"].update_one({'email': email_address},{'$set': update} )
            else:
                # otherwise, get the last pull time from the database
                start_datetime = email_document['timestamp']
            end_datetime = datetime.now(pytz.utc)

            # Set up IMAP
            imap_server = 'imap.gmail.com'
    
            imap = imaplib.IMAP4_SSL(imap_server)
            imap.login(email_address, email_secret)

            imap.select('Inbox')
    

            start_datetime = datetime.now(pytz.utc) - timedelta(hours=120)
            end_datetime = datetime.now(pytz.utc) - timedelta(hours=60)
            start_date_str = start_datetime.strftime("%d-%b-%Y")
            end_date_str = end_datetime.strftime("%d-%b-%Y")
            imap.select('Inbox')
    

            # pulling emails since since_date var hours ago
            def get_emails_since(con, since, before):
                result, data = con.search(None, 'SINCE', since, 'BEFORE', before)
                return data
    

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

            account_data = {
                    "account_string": username,
                    "account_address": email_address,
                    "bot_sorted_collection_string": bot_sort_string,
                    "email_id": "",
                }
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

            try:
                last_email = email_collection.find_one(sort=[('iterative_value', -1)])
                last_iterative_value = last_email['iterative_value']
            except (TypeError, KeyError):
                last_iterative_value = 0

            # Extracted emails will be stored in this list:
            emails_list = []




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

                sorted_emails_list = sorted(emails_list, key=lambda x: datetime.strptime(x['email_date'], '%d %b %Y %H:%M:%S %z'))

                # Add iterative value based on position in the sorted list
                for idx, email_data_item in enumerate(sorted_emails_list, start=last_iterative_value + 1):
                    email_data_item['iterative_value'] = idx
                    email_collection.insert_one(email_data_item)
                    bot_sorted_collection.insert_one(email_data_item)
                    account_data["email_id"] = email_data_item["email_id"]
                    j_account_data = json.dumps(account_data)
                    print(f"send to bot {email_data_item['email_id']}")
                    bot_sort.categorize_emails(j_account_data)

                account_data["email_id"] = email_id
                j_account_data = json.dumps(account_data)

                email_collection.insert_one(email_data)
                #last_email_pull_collection.update_one({'_id': 'last_pull_time'}, {'$set': {'datetime': end_datetime}})
                bot_sorted_collection.insert_one(email_data)
                print(f"send to bot {email_id}")
                bot_sort.categorize_emails(j_account_data)
            # Inserting email data into database
            
            imap.close()
    
    
if __name__ == '__main__':
     get_emails()
    

    