from bson import json_util, ObjectId
from flask import Flask, request, jsonify
from flask_cors import CORS
import configparser
from pymongo import MongoClient
import sys
import base64
import uuid
import datetime
sys.path.append("C:\\Users\\casey\\PycharmProjects\\email_sort\\")
import pull_emails
from resort_emails import resort_emails
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from account_change import add_new_email
from os import abort

# Flask settings
app = Flask(__name__)
CORS(app)  # Enable CORS for the Flask app
app.config['JWT_SECRET_KEY'] = '2a56363f-1c5a-434c-bd23-a8b157383ce9'
jwt = JWTManager(app)
CORS(app)



# Read settings from a configuration file


# Get MongoDB settings from the config file

# Get MongoDB connection and collections
client = MongoClient("mongodb://localhost:27017/")
db = client['emails']
debugDB = client['debug']




debug_collection = debugDB['email_server']
debug_id = str(uuid.uuid4())
debug_filter = {"debug_id": debug_id}
debug_collection.insert_one(debug_filter)

@app.route('/email_add', methods=['POST'])
@jwt_required()
def add_email():
    current_user = get_jwt_identity()
    data = request.get_json()  # Get data sent to the endpoint
    email = data.get('email')
    password = data.get('password')

    # Run the email_add.py script with email and password as arguments
    add_new_email(current_user,email, password)

    return jsonify({'message': 'Successfully ran email_add.py'}), 200



@app.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        debug_id = str(uuid.uuid4())
        debug_filter = {"debug_id": debug_id}
        current_user = get_jwt_identity()
        debug_collection.insert_one(debug_filter)
        debug_collection.update_one(debug_filter, {'$set': {'user': current_user}})
        user_db = client[current_user]
        account_collection = user_db["acc_info"]
        user_info = account_collection.find_one({}, {'_id': 0})

        if user_info is None:
            abort(404, description="User info not found")
        else:
            return jsonify(user_info), 200
    except Exception as e:
        debug_collection.update_one(debug_filter, {'$set': {'errors': e}})  # Consider logging this to a log file for production code
        abort(500, description="Internal Server Error")
    
    except Exception as e:
        return jsonify({'error': f'Failed to get user profile: {str(e)}'}), 500
    user = get_jwt_identity()
    user_db = client[user]
    account_collection = user_db["acc_info"]
    user_info = account_collection.find_one()
    if user:
        return jsonify(user_info), 200
    else:
        return {"error": "User not found"}, 404
@app.route('/api/resort-emails', methods=['GET'])
@jwt_required() 
def resort_emails_endpoint():
    current_user = get_jwt_identity()
    try:
        resort_emails(current_user)
        return jsonify({'message': 'Emails resorted successfully.'}), 200
    except Exception as e:
        print(f"Error running resort_emails: {e}")
        return jsonify({'error': f'Failed to resort emails: {str(e)}'}), 500



@app.route('/api/refresh-emails', methods=['GET'])
@jwt_required() 
def refresh_emails():
    current_user = get_jwt_identity()
    try:
        pull_emails.get_emails(current_user)
        return jsonify({'message': 'Emails refreshed successfully.'}), 200
    except Exception as e:
        f = open("refreshdebug.txt", "w")
        f.write(str(e))
        return jsonify({'error': f'Failed to refresh emails: {str(e)}'}), 500

#Gather emails from the database
@app.route('/api/get-emails', methods=['GET'])
@jwt_required()
def get_emails():
    current_user = get_jwt_identity()
    
    
    user_db = client[current_user]
    email_accounts_cursor = user_db['email_accounts'].find({})
    
    emails_by_account = {}

    for email_account in email_accounts_cursor:
        email_address = email_account['email']
        botSortString = email_address + "_bot_sort"
        account_collection = user_db[botSortString] # Here, each email account corresponds to a collection in the database

        emails_by_account[email_address] = list(account_collection.find())

    return json_util.dumps(emails_by_account), 200




@app.route('/api/move-email', methods=['POST'])
@jwt_required() 
def update_email():
    data = request.get_json()
    debug_id = str(uuid.uuid4())
    debug_filter = {"debug_id": debug_id}
    debug_collection.update_one(debug_filter, {'$set': {'runInfo': "Running move email"}})
    current_user = get_jwt_identity()
    
   
    debug_collection.update_one(debug_filter, {'$set': {'user': current_user}})
    
    email_id = ObjectId(data['email']['_id'])
    debug_collection.update_one(debug_filter, {'$set': {'email_id': email_id}})
    
    user_database = client[current_user]
    user_collection  = user_database["emails"]
    bot_sorted_collection = user_database["bot_sorted"]
    user_sorted_collection = user_database["re-sorted"]
    # Insert the updated email into the body collection
    try:
        filter = { '_id': email_id }
        update = { '$set': { f"completion": data['email']['completion'] } }
        try:
            old_email = bot_sorted_collection.find_one(filter)
            bot_sorted_collection.delete_one(filter)
        except old_email == None: 
            old_email = user_collection.find_one(filter)
            user_collection.delete_one(filter)
        
        
        user_sorted_collection.insert_one(old_email)
        user_sorted_collection.update_one(filter, update)
        user_collection.delete_one(filter)
    except Exception as e:
        print(f"Error inserting email: {e}")
        return jsonify({'error': f'Failed to insert email: {str(e)}'}), 500

    return jsonify({'message': 'Email moved successfully.'}), 200


@app.route('/api/delete-email', methods=['POST'])
def delete_email():
    data = request.get_json()
    current_user = get_jwt_identity()
    user_database = client[current_user]
    user_collection  = user_database["emails"]
    bot_sorted_collection = user_database["bot_sorted"]
    user_sorted_collection = user_database["re-sorted"]
    email_id = ObjectId(data['email']['_id'])
    print(f"Email ID: {email_id}")  # Print the email_id to check its value

    # Delete the email from the database
    try:
        user_sorted_collection.delete_one({'_id': email_id})
        return jsonify({'message': 'Email deleted successfully.'}), 200
    except Exception as e:
        print(f"Error deleting email from user_sorted_collection: {e}")
        # Return immediately after an error occurs
        return jsonify({'error': f'Failed to delete email from user_sorted_collection: {str(e)}'}), 500

    try:
        bot_sorted_collection.delete_one({'_id': email_id})
        return jsonify({'message': 'Email deleted successfully.'}), 200
    except Exception as e:
        print(f"Error deleting email from bot_sorted_collection: {e}")
        return jsonify({'error': f'Failed to delete email from bot_sorted_collection: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(port=3001)
