import imaplib, email, json, os, base64, uuid
from datetime import datetime, timedelta
import secrats
from pymongo import MongoClient

#Change this later to take in token from auth server and associate it with database entries
user = 'greenturtlekava@gmail.com'
password = "qrobdjbyllkrlphx"
imap_url = 'imap.gmail.com'
directory = "front-end\\email-review\\public\\unsorted"
mongo_uri = "mongodb://localhost:27017/"
database_name = "Emails"
unsorted_collection = "unsorted"

account_bytes = base64.b64encode(password.encode('utf-8'))
account_string = account_bytes.decode('utf-8')

encoded_bytes = base64.b64encode(user.encode('utf-8'))
encoded_address = encoded_bytes.decode('utf-8')


client = MongoClient(mongo_uri)
db = client[account_string]
address_collection = db[encoded_address]




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
since_date = datetime.now() - timedelta(hours=60)
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

    address_collection.insert_one(email_data)

