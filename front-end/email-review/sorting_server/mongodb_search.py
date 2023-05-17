import configparser
from pymongo import MongoClient
config = configparser.ConfigParser()
config.read('config.ini')
mongo_uri = "mongodb://localhost:27017/"
database_name = "Emails"
body_collection = "Bodied"
bodyless_collection = "bodyless_emails"
client = MongoClient(mongo_uri)
db = client[database_name]
body_collection_db = db[body_collection]
bodyless_collection_db = db[bodyless_collection]
query = { "completion": { "$regex": ".*T.*" } }
results = bodyless_collection_db.find(query)

# Iterate over the results
for result in results:
    print(result)

results = body_collection_db.find(query)

for result in results:
    print(result)

# Close the MongoDB connection
client.close()