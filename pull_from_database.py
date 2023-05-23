from pymongo import MongoClient
import json

# Replace 'your_database' and 'your_collection' with your actual database and collection names
database_name = "Emails"
collection_name = "prime_emails"

# Create a MongoClient to the running mongod instance
client = MongoClient('localhost', 27017)
db = client[database_name]

# Get your collection from the database
collection = db[collection_name]

# Fetch all documents from the collection
documents = collection.find()

# Convert MongoDB Cursor to list of dicts
documents_list = list(documents)

# Remove the '_id' key from each document
for document in documents_list:
    document.pop('_id', None)

# Write the documents to a json file
with open('train_gpt_data_prime.json', 'w') as file:
    file.write(json.dumps(documents_list, indent=4))
