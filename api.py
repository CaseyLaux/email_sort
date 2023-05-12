import imaplib
import email
from email.header import decode_header
import openai

# Set up OpenAI API key
openai.api_key = "your_openai_api_key_here"


# Function to categorize email titles
def categorize_titles(titles):
    prompt = "Generate categories for the following email titles:\n" + "\n".join(titles)

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.5,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    categories = response.choices[0].text.strip().split("\n")

    return categories


# Login to your email account
email_user = "your_email@example.com"
email_password = "your_email_password"
imap_url = "imap.example.com"

mail = imaplib.IMAP4_SSL(imap_url)
mail.login(email_user, email_password)

# Select the mailbox you want to read
mail.select("inbox")

# Search for all emails
_, all_emails = mail.search(None, "ALL")

# Get the list of email IDs
email_ids = all_emails[0].split()

# Read email titles
email_titles = []
for e_id in email_ids:
    _, msg_data = mail.fetch(e_id, "(BODY[HEADER.FIELDS (SUBJECT)])")
    raw_msg = msg_data[0][1]
    msg = email.message_from_bytes(raw_msg)
    subject = decode_header(msg["Subject"])[0]
    if isinstance(subject[0], bytes):
        subject = subject[0].decode(subject[1])
    email_titles.append(subject)

# Categorize email titles
categories = categorize_titles(email_titles)

# Print the generated categories
print("Generated categories:")
print("\n".join(categories))

# Logout and close the connection
mail.logout()
