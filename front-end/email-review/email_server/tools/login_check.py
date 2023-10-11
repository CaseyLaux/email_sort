import imaplib
from pymongo import MongoClient



def check_login(username):
    mongo_uri = "mongodb://localhost:27017/"
    client = MongoClient(mongo_uri)
    imap = imaplib.IMAP4_SSL('imap.gmail.com')

# Dictionary to store username as key and list of email addresses as value
    user_email_dict = {}

    
    
    user_db = client[username]
    email_accounts = user_db['email_accounts'].find({})
        
    # Fetch email addresses and store in the dictionary
    email_list = [
    {'email': email_account['email'], 'secret': email_account['secret']} 
    for email_account in email_accounts 
    if 'email' in email_account and 'secret' in email_account
    ]
    user_email_dict[username] = email_list
    try:
        for email_detail in email_list:
            imap.login(email_detail['email'], email_detail['secret'])
    except imaplib.IMAP4.error:
        return f"Invalid credentials for user{username} email {email_detail['email']}"
    return True
