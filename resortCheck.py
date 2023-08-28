from pymongo import MongoClient, ASCENDING

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['eggsj']  # Make sure to use the corrected username here
collection = db['caseyLaux631@gmail.com_bot_sort']

# Fetch all documents sorted by 'parsed_email_date' in ascending order
sorted_documents = list(collection.find().sort('parsed_email_date', ASCENDING))

# Print 'iterative_value' and 'parsed_email_date' for each document
for document in sorted_documents:
    print(f"Iterative Value: {document['iterative_value']}, Date: {document['parsed_email_date']}")
