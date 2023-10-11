from bson import json_util, ObjectId
from flask import Flask, request, jsonify
from flask_cors import CORS
import configparser
from pymongo import MongoClient
from tools.resort_emails import resort_emails
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from account_change import add_new_email
from os import abort
import sys
from tools.convertCLASS_RATING import find_classification_and_rating
from tools.login_check import check_login
# Flask settings
app = Flask(__name__)
CORS(app)  # Enable CORS for the Flask app
app.config['JWT_SECRET_KEY'] = '2a56363f-1c5a-434c-bd23-a8b157383ce9'
jwt = JWTManager(app)



# Read settings from a configuration file


# Get MongoDB settings from the config file

# Get MongoDB connection and collections
client = MongoClient("mongodb://localhost:27017/")
db = client['emails']


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

        current_user = get_jwt_identity()
        user_db = client[current_user]
        account_collection = user_db["acc_info"]
        user_info = account_collection.find_one({}, {'_id': 0})

        if user_info is None:
            abort(404, description="User info not found")
        else:
            return jsonify(user_info), 200
    except Exception as e:
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


@app.route('/api/emailcheck', methods=['POST'])
@jwt_required()
def login_check():
    current_user = get_jwt_identity()
    loginSuccess = check_login(current_user)
    
    if loginSuccess == True:
        return jsonify({'message': 'Email matches current user.'}), 200
    else:
        return jsonify({'error': f'{loginSuccess}'}), 401



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




@app.route('/api/update-email', methods=['POST'])
@jwt_required() 
def update_email():
    data = request.get_json()
    current_user = get_jwt_identity()
    email_id = ObjectId(data['_id'])
    email_account = data['email_account']
    user_database = client[current_user]
    bot_sorted_string = email_account + "_bot_sort"
    resortString = email_account + "_re-sort"
    user_collection  = user_database[bot_sorted_string]
    user_sorted_collection = user_database[resortString]
    completion = data['completion']
    classification, rating = find_classification_and_rating(completion)
    print(f"classification: {classification}")
    print(f"rating: {rating}")
    print(f"email id {email_id}")
    # Insert the updated email into the body collection
    try:
        filter = { '_id': email_id }
        update = { '$set': { "completion": completion, "category": classification, "rating": rating } }
        try:
            old_email = user_collection.find_one(filter)
            if old_email:
                user_collection.delete_one(filter)
                user_collection.insert_one(old_email)
                user_collection.update_one(filter, update)
            else:
                print("Email not found!")
        except old_email == None: 
            print("error test")
            old_email = user_collection.find_one(filter)
            user_collection.delete_one(filter)
        
        user_sorted_collection.insert_one(old_email)
        user_sorted_collection.update_one(filter, update)
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
