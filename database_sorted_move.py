from pymongo import MongoClient

# create a connection to MongoDB
client = MongoClient('mongodb://localhost:27017/')

# specify the database and the collections
db = client['cXJvYmRqYnlsbGtybHBoeA==']
source_collection = db['Z3JlZW50dXJ0bGVrYXZhQGdtYWlsLmNvbQ==']
target_collection = db['Z3JlZW50dXJ0bGVrYXZhQGdtYWlsLmNvbQ==_rated']

# find all documents where 'completion' is not null
query = {"completion": {"$ne": ' '}}

# loop through each document in the source collection
for document in source_collection.find(query):
    # move the document to the target collection
    target_collection.insert_one(document)
    
    # delete the document from the source collection
    source_collection.delete_one({"_id": document["_id"]})

print("Emails moved successfully!")
