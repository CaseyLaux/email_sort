def add_new_email(user, email, password):
    from pymongo import MongoClient

    # Connection URL
    client = MongoClient('mongodb://localhost:27017/')

    # Select the database
    db = client[user]

    # Select the collection within the database
    accounts = db['email_accounts']
    
    # User data
    user = {
        'email': email,
        'secret': password,  # this should be hashed in a real application
        'new_account': True
    }

    # Insert a document into the collection
    accounts.insert_one(user)

    print('User added successfully')
