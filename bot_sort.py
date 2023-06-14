import sys
import imaplib
import email
from email.header import decode_header
import openai
from pymongo import MongoClient
import json
import time
import logging

# Set up logging
logging.basicConfig(filename='bot_sort_debug.txt', level=logging.DEBUG)

# Set up OpenAI API key 
def clean_string(input_string):
        if len(input_string) > 1000:
            # If so, truncate it to the first 1000 characters
            input_string = input_string[:1000]
# Function to categorize email titles
def categorize_emails(i_account_data):
    logging.debug('Starting categorize_emails function')
    i_j_account_data = json.loads(i_account_data)
    mongo_uri = "mongodb://localhost:27017/"
    database = i_j_account_data["account_string"]
    collection_name = i_j_account_data["bot_sorted_collection_string"]
    client = MongoClient(mongo_uri)
    db = client[database]
    collection = db[collection_name]
    filter = {"email_id": i_j_account_data["email_id"]}
    t=0
    email = None
    while email==None:
        if t>100:
            exit(print("Error: Email not found"))
        try:
            email = collection.find_one(filter)
        except email==None:
            t+=5
            time.sleep(5)

    logging.debug(f'Email: {email}')
    prompt = email["prompt"]
    openai.api_key = "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"
    response = openai.Completion.create(
        engine="ada:ft-personal:new-prime-2023-06-07-01-27-19",
        prompt=prompt,
        temperature=0.5,
        max_tokens=2,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    categories = response.choices[0].text.strip().split("\n")
    logging.debug(f'{prompt                                                                                                             }: {categories}')

    categories = str(categories).replace('#', '')
    categories = categories.replace(' ', '')
    categories = categories.replace('[', '')
    categories = categories.replace(']', '')
    categories = categories.replace("'", '')

    collection.update_one(filter, {"$set": {"completion": categories}})
    return 
