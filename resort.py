from pymongo import MongoClient, ASCENDING
from email.utils import parsedate_to_datetime

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['Colin']
collection = db['greenturtlekava@gmail.com_bot_sort']
print(collection.find_one())
# Fetch all documents and convert the email_date to datetime objects
documents = list(collection.find())
for document in documents:
    # Convert the 'email_date' string to a Python datetime object
    dt = parsedate_to_datetime(document['email_date'])
    # Update the document in the collection with the datetime object
    collection.update_one({'_id': document['_id']}, {'$set': {'parsed_email_date': dt}})

# Fetch all documents sorted by 'parsed_email_date' in ascending order
sorted_documents = list(collection.find().sort('parsed_email_date', ASCENDING))

# Update each document to add an iterative counter
for idx, document in enumerate(sorted_documents):
    print("test")
    collection.update_one({'_id': document['_id']}, {'$set': {'iterative_value': idx + 1}})

print("Documents updated!")
