import sys
import imaplib
import email
from email.header import decode_header
import openai
from pymongo import MongoClient
import json
import time


# Set up OpenAI API key 
def clean_string(input_string):
        if len(input_string) > 1000:
            # If so, truncate it to the first 1000 characters
            input_string = input_string[:1000]

# Function to categorize email titles
def categorize_emails(i_account_data):
    CLASSIFICATION_VALUES = {
        "Spam": 29,
        "Marketing": 31,
        "Events": 37,
        "Delivery": 41,
        "Analytics": 43,
        "Business": 47,
        "Invoice": 53,
        "Urgent": 59,
    }

    RATING_VALUES = {
        1: 2,
        2: 3,
        3: 5,
        4: 7,
        5: 11,
        6: 13,
        7: 17,
        8: 19,
        9: 23,
    }
    def get_rating_and_category(value):
        for rating, rating_prime in RATING_VALUES.items():
            if value % rating_prime == 0:
                for category, category_prime in CLASSIFICATION_VALUES.items():
                    if value / rating_prime == category_prime:
                        return rating, category
        return 0, "RATING_ERROR"
    i_j_account_data = json.loads(i_account_data)
    mongo_uri = "mongodb://localhost:27017/"
    database = i_j_account_data["account_string"]
    collection_name = i_j_account_data["bot_sorted_collection_string"]
    client = MongoClient(mongo_uri)
    db = client[database]
    collection = db[collection_name]
    filter = {"email_id": i_j_account_data["email_id"]}
    print(filter)
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
    categories = str(categories).replace('#', '')
    categories = categories.replace(' ', '')
    categories = categories.replace('[', '')
    categories = categories.replace(']', '')
    categories = categories.replace("'", '')
    if categories == '':
        categories = '0'
    print(categories)
    rating, category = get_rating_and_category(int(categories))
    print(rating)
    print(category)
    collection.update_one(filter, {"$set": {"completion": categories}})
    collection.update_one(filter, {"$set": {"rating": rating}})
    collection.update_one(filter, {"$set": {"category": category.lower()}})
    return 
