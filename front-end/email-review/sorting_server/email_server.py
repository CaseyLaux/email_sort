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
from secrats import ColinGTK
import pull_emails
from resort_emails import resort_emails
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

# Flask settings
app = Flask(__name__)
CORS(app)  # Enable CORS for the Flask app
app.config['JWT_SECRET_KEY'] = '2a56363f-1c5a-434c-bd23-a8b157383ce9'
jwt = JWTManager(app)
CORS(app)



# Read settings from a configuration file
config = configparser.ConfigParser()
config.read('./sorting_server/config.ini')

# Get MongoDB settings from the config file
mongo_settings = {key: config.get('mongo', key) for key in ['uri', 'database', 'body_collection', 'bodyless_collection', 'unsorted_collection']}

# Get MongoDB connection and collections
client = MongoClient(mongo_settings['uri'])
db = client[mongo_settings['database']]
debugDB = client['debug']


user_database = client[ColinGTK().Account_ID]
user_collection = user_database[ColinGTK().user]
user_sorted_string = ColinGTK().user + 're-sorted'
user_sorted_collection = user_database[user_sorted_string]


bot_sorted_string = ColinGTK().user + '_bot_sorted'
bot_sorted_collection = user_database[bot_sorted_string]

debug_collection = debugDB['email_server']
debug_id = str(uuid.uuid4())
debug_filter = {"debug_id": debug_id}
debug_collection.insert_one(debug_filter)


@app.route('/api/resort-emails', methods=['GET'])
@jwt_required() 
def resort_emails_endpoint():
    try:
        resort_emails()
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
    debug_collection.update_one(debug_filter, {'$set': {'runInfo': "Running get emails"}})
    try:
        debug_collection.update_one(debug_filter, {'$set': {'user': current_user}})
    except Exception as e:
        debug_collection.update_one(debug_filter, {'$set': {'errors': e}})
    user_database = client[current_user]
    user_collection  = user_database["emails"]
    bot_sorted_collection = user_database["bot_sorted"]


    user_sorted_emails = list(user_sorted_collection.find())
    user_unsorted_emails = list(user_collection.find())
    bot_sorted_emails = list(bot_sorted_collection.find())
    debug_collection.update_one(debug_filter, {'$set': {'emails': user_sorted_emails}})
    
    return json_util.dumps({'user_sorted_emails':user_sorted_emails, 'user_unsorted_emails': user_unsorted_emails, 'bot_sorted_emails': bot_sorted_emails}), 200



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
    app.run(port=config.getint('app', 'port'))