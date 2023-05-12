import imaplib, email, json, os
from datetime import datetime, timedelta

user = 'greenturtlekava@gmail.com'
password = 'hjolwtqwkwnhzhjp'
imap_url = 'imap.gmail.com'
directory = "front-end\\email-review\\public\\unsorted"


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


def get_latest_email_number():
    files = os.listdir(directory)
    max_number = 0
    for file in files:
        if file.startswith("email_") and file.endswith(".txt"):
            number = int(file[6:-4])
            if number > max_number:
                max_number = number
    return max_number


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

latest_email_number = get_latest_email_number()

for i in range(len(senders)):
    email_data = {
        "prompt": f"Subject: {subjects[i]}\nFrom:{senders[i]}\nTo:support@ourcompany.com\nDate:{dates[i]}\nContent:{bodies[i].decode('utf-8', errors='replace')}\n###\n\n",
        "completion": " ",
        "email_subject": subjects[i],
        "email_sender": senders[i],
        "email_date": dates[i]
    }

    email_number = latest_email_number + i + 1
    with open(f"{directory}/email_{email_number}.txt", "w", encoding="utf-8") as f:
        f.write(json.dumps(email_data, ensure_ascii=False, indent=2))

    print(f"Saved email {email_number} to {directory}/email_{email_number}.json")
