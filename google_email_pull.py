import imaplib, email, json, os, base64, uuid
from datetime import datetime, timedelta
from secrats import decrypt_secrets, ColinGTK
from pymongo import MongoClient
import bot_sort
#Change this later to take in token from auth server and associate it with database entries
user, password = decrypt_secrets()
imap_url = 'imap.gmail.com'
directory = "front-end\\email-review\\public\\unsorted"
mongo_uri = "mongodb://localhost:27017/"
database_name = "Emails"
unsorted_collection = "unsorted"

#Set vars

account_instance = ColinGTK()
account_string = account_instance.Account_ID
account_address = account_instance.user
bot_sorted_collection_string = (str(account_address) + "_bot_sorted") 

#Connect to database
client = MongoClient(mongo_uri)
db = client[account_string]
address_collection = db[account_address]


#Create collections
bot_sorted_collection = db[bot_sorted_collection_string]

account_data = {
    "account_string": account_string,
    "account_address": account_address,
    "bot_sorted_collection_string": bot_sorted_collection_string,
    "email_id": "",
    "prompt": ""
}
def clean_string(input_string):
    if len(input_string) > 1000:
        # If so, truncate it to the first 1000 characters
        input_string = input_string[:1000]

    return input_string

def get_body(msg):
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None, True)


def search(key, value, con):
    result, data = con.search(None, key, '"{}"'.format(value))
    return data


def get_emails(result_bytes):
    msgs = []
    for num in result_bytes[0].split():
        typ, data = con.fetch(num, '(RFC822)')
        msgs.append(data)
    return msgs


def get_emails_since(con, since, before):
    result, data = con.search(None, 'SINCE', since.strftime('%d-%b-%Y'), 'BEFORE', before.strftime('%d-%b-%Y'))
    return data


con = imaplib.IMAP4_SSL(imap_url)
con.login(user, password)
con.select('Inbox')

# Calculate the date 12 hours ago
since_date = datetime.now() - timedelta(hours=24)
before_date = datetime.now() - timedelta(hours=0)

msgs = get_emails(get_emails_since(con, since_date, before_date))

senders = []
subjects = []
bodies = []
dates = []

for msg in msgs[::-1]:
    for sent in msg:
        if type(sent) is tuple:
            content = str(sent[1], 'utf-8', errors='replace')
            mail = email.message_from_string(content)

            sender = mail["From"]
            subject = mail["Subject"]
            date = mail["Date"]
            body = get_body(mail)
            body = clean_string(body)
            
            senders.append(sender)
            subjects.append(subject)
            dates.append(date)
            bodies.append(body)


for i in range(len(senders)):
    email_id = str(uuid.uuid4())
    email_data = {
        "prompt": f"Subject: {subjects[i]}\nFrom:{senders[i]}\nTo:support@ourcompany.com\nDate:{dates[i]}\nContent:{bodies[i].decode('utf-8', errors='replace')}\n###\n\n",
        "completion": " ",
        "email_subject": subjects[i],
        "email_sender": senders[i],
        "email_date": dates[i],
        "email_id": email_id,

    }
    account_data["email_id"] = email_id
    j_account_data = json.dumps(account_data)
    address_collection.insert_one(email_data)
    bot_sorted_collection.insert_one(email_data)
    bot_sort.categorize_emails(j_account_data)
    


