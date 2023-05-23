from pymongo import MongoClient
import json
# Create a client connection to your MongoDB instance
client = MongoClient('mongodb://localhost:27017/')

# Connect to your database
db = client['Emails']

# Connect to your existing collection
collection = db['bodyless_emails']

# Create a new collection
new_collection = db['prime_emails']

# Find all documents where 'completion' field contains 'Classification: Analytics'
# Assuming 'completion' is a string, and 'Classification: Analytics' is part of it


def analytic_prime_emails():
    x = 0
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    while x < 10:
        x += 1
        result = collection.find({'completion': f"Classification: Analytics, Rating: {x}"})
        new_prime = 43 * primes[x - 1]
        prime_emails = db.new_collection

        for doc in result: 
            doc.pop('_id', None)
            doc['completion'] = new_prime
            new_collection.insert_one(doc)


def marketing_prime_emails():
    x = 0
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    while x < 10:
        x += 1
        result = collection.find({'completion': f"Classification: Marketing, Rating: {x}"})
        new_prime = 31 * primes[x - 1]
        prime_emails = db.new_collection

        for doc in result: 
            doc.pop('_id', None)
            doc['completion'] = new_prime
            new_collection.insert_one(doc)

def urgent_prime_emails():
    x = 0
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    while x < 10:
        x += 1
        result = collection.find({'completion': f"Classification: Urgent, Rating: {x}"})
        new_prime = 59 * primes[x - 1]
        prime_emails = db.new_collection

        for doc in result: 
            doc.pop('_id', None)
            doc['completion'] = new_prime
            new_collection.insert_one(doc)
def business_prime_emails():
    x = 0
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    while x < 10:
        x += 1
        result = collection.find({'completion': f"Classification: Business, Rating: {x}"})
        result = collection.find({'completion': f"Classification: business, Rating: {x}"})
        result = collection.find({'completion': f"Classification: bussiness, Rating: {x}"})
        result = collection.find({'completion': f"Classification: Bussiness, Rating: {x}"})
        new_prime = 47 * primes[x - 1]
        prime_emails = db.new_collection

        for doc in result: 
            doc.pop('_id', None)
            doc['completion'] = new_prime
            new_collection.insert_one(doc)
def invoice_prime_email():
    x = 0
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    while x < 10:
        x += 1
        result = collection.find({'completion': f"Classification: Invoice, Rating: {x}"})
        new_prime = 53 * primes[x - 1]
        prime_emails = db.new_collection

        for doc in result: 
            doc.pop('_id', None)
            doc['completion'] = new_prime
            new_collection.insert_one(doc)

def sort():
    urgent_prime_emails()
    business_prime_emails()
    invoice_prime_email()
    marketing_prime_emails()
    analytic_prime_emails()
sort()