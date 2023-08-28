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
import time

# Setting up logging vars


# Setting up login creds for user



def get_emails():
    

    # Setting up vars for database
    mongo_uri = "mongodb://localhost:27017/"
    client = MongoClient(mongo_uri)


    
    users_db = client['ai']
    users = users_db['users'].find({})
    for user in users:
        username = user['username']
        print(username)
        user_db = client[username]
        email_accounts = user_db['email_accounts'].find({}) 
        for email_account in email_accounts:
            email_address = email_account['email']
            email_secret = email_account['secret']
            email_collection = user_db[email_address]
            bot_sort_string = email_address + "_bot_sort"
            bot_sorted_collection = user_db[bot_sort_string]
            email_document = user_db["email_accounts"].find_one({'email': str(email_address)})
            try:
                last_timestamp_doc = email_document["timestamp"]
                print(f"{last_timestamp_doc} test")
            except KeyError:
                last_timestamp_doc = None
            
            if last_timestamp_doc is None:
                # if it's the first time, default to 120 hours ago
                start_datetime = datetime.now(pytz.utc) - timedelta(hours=120)
                start_datetime = start_datetime.timestamp()
                # create document
                update = {'timestamp': start_datetime}
                user_db["email_accounts"].update_one({'email': email_address},{'$set': update} )
            else:
                # otherwise, get the last pull time from the database
                start_datetime = last_timestamp_doc
            end_datetime = datetime.now(pytz.utc)

            # Set up IMAP
            imap_server = 'imap.gmail.com'
    
            imap = imaplib.IMAP4_SSL(imap_server)
            imap.login(email_address, email_secret)

            imap.select('Inbox')
    
                #Uncomment to test 24 hour pull
            #start_datetime = datetime.now(pytz.utc) - timedelta(hours=24)
            end_datetime = datetime.now(pytz.utc)
            
            end_date_str = end_datetime.strftime("%d-%b-%Y")
            imap.select('Inbox')
            def unix_timestamp_to_datetime(timestamp):
                return datetime.utcfromtimestamp(int(timestamp))
            
            def format_datetime_for_imap(dt_object):
                return dt_object.strftime("%d-%b-%Y")
            
            # pulling emails since since_date var hours ago
            def get_emails_since(con, since_unix, before_unix):
                since_datetime = unix_timestamp_to_datetime(since_unix)
                
                since_str = format_datetime_for_imap(since_datetime)
                before_str = before_unix
                print(f"since {since_str} before {before_unix}")
                
                result, data = con.search(None, 'SINCE', since_str, 'BEFORE', before_str)
                return data
    

            # Using search results to pull emails since since_date
            search_results = get_emails_since(imap, start_datetime, end_date_str)
            def decode_content(part):
                # Pull charset and encoding to decode body text
                charset = part.get_content_charset()  # Get the charset
                encoding = part.get('Content-Transfer-Encoding')  # Get the encoding

                

                if charset is None:
                    charset = 'utf-8'  # Use a default charset if none is specified
                
                payload = part.get_payload(decode=True)

                
                payload = payload.decode(charset, errors='replace')
                clean_body = payload.replace('  ', '').replace('\r', '').replace('\u200c', '').replace('\u0020', '')
            
                if payload is None:
                    payload =  ''
                if len(clean_body) > 1000:
                    clean_body = clean_body[:1000]
                #clean_body = clean_body.decode(charset)
                return payload, clean_body
            def decode_header_value(value):
                decoded_header = decode_header(value)
                header_parts = []
                
                for decoded_string, encoding in decoded_header:
                    if isinstance(decoded_string, bytes):
                        if encoding:
                            old_string = decoded_string
                            decoded_string = decoded_string.decode(encoding)

                        else:
                            old_string = decoded_string
                            encoding = 'utf-8'
                            decoded_string = decoded_string.decode('utf-8')


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
            email_unix_time = []
            test_array = []
            html_bodies = []
            i = 0
            result = bot_sorted_collection.find().sort("iterative_value", -1).limit(1)
            for doc in result:
                try:
                    last_iterative_value = doc['iterative_value']
                except KeyError:
                    last_iterative_value = 1    
            try:
                last_iterative_value += 1
            except UnboundLocalError:
                last_iterative_value = 1
            # Parse through data from email pull
            for search_results in search_results[0].split():
                _, data = imap.fetch(search_results, '(RFC822)')
                email_message = email.message_from_bytes(data[0][1])
                email_unix_timestamp = email.utils.mktime_tz(email.utils.parsedate_tz(email_message.get('Date')))
                if email_unix_timestamp <= start_datetime:
                    continue
                i += 1
                
                

                senders.append(email_message.get('From'))
                subject = email_message.get('Subject')
                clean_subject = decode_header_value(subject)
                subjects.append(clean_subject)
                dates.append(email_message.get('Date'))
                email_unix_time.append(email.utils.mktime_tz(email.utils.parsedate_tz(email_message.get('Date'))))

                
                
                
                clean_body_parts = []
                body_parts = []
                html_body_parts = []
                for part in email_message.walk():
                    if part.get_content_type() == 'text/plain':
                        body, clean_body = decode_content(part)
                        body_parts.append(body)
                        # Add the cleaned body parts to clean_body_parts as well
                        clean_body_parts.append(clean_body)
                    elif part.get_content_type() == 'text/html':
                        body, clean_body = decode_content(part)
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

                bodies.append(body)
                clean_bodies.append(clean_body)
                html_bodies.append(html_body)
            i = 0

            

            # Extracted emails will be stored in this list:

            

            emails = []

# 1. Collect all the emails into a list.
            for i in range(len(subjects)):
                email_id = str(uuid.uuid4())
                email_data = {
                    "prompt": f"Subject: {subjects[i]}\nFrom:{senders[i]}\nTo:support@ourcompany.com\nDate:{dates[i]}\nContent:{clean_bodies[i]}\n###\n\n",
                    "completion": " ",
                    "email_subject": subjects[i],
                    "email_sender": senders[i],
                    "email_date": dates[i],
                    "email_unix_time": email_unix_time[i],
                    "email_id": email_id,
                    "body": bodies[i],
                    "html_body": html_bodies[i]
                }
                
                emails.append(email_data)

            # 2. Sort the emails based on the timestamp.

            sorted_emails = sorted(emails, key=lambda x: x["email_unix_time"], reverse=True)
           
            
            try:
                email_with_largest_iterative = sorted_emails[0]
                largest_timestamp = email_with_largest_iterative["email_date"]
            except IndexError:
                largest_timestamp = "No emails"
            # 3. Iterate through the sorted emails, assign an iterative number, and then store the email data with the assigned number.
            for idx, email_data in enumerate(sorted_emails):
                idx + last_iterative_value
                email_data["iterative_number"] = idx + 1

                account_data["email_id"] = email_data["email_id"]
                j_account_data = json.dumps(account_data)

                email_collection.insert_one(email_data)
                bot_sorted_collection.insert_one(email_data)
                largest_unix_timestamp_moment = max(email_unix_time)
                print(f"{email_data['email_unix_time']} {largest_unix_timestamp_moment}")

                bot_sort.categorize_emails(j_account_data)

                # assuming user_db and email_address have been defined earlier in your code
            
            try:
                largest_unix_timestamp = max(email_unix_time)
                user_db["email_accounts"].update_one({'email': email_address}, {'$set': {'timestamp': largest_unix_timestamp}})
                print(largest_unix_timestamp)
            except ValueError:
                largest_unix_timestamp = start_datetime
            amountOfEmails = len(sorted_emails)
            print(f"Found {amountOfEmails} new emails for {email_address}")
            user_db["email_accounts"].update_one({'email': email_address}, {'$set': {'timestamp': largest_unix_timestamp}})
            imap.close()
    
    
if __name__ == '__main__':
     get_emails()
    

    