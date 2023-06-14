from bson import json_util, ObjectId
from flask import Flask, request, jsonify
from flask_cors import CORS
import configparser
from pymongo import MongoClient
import sys
import base64
import uuid
sys.path.append("C:\\Users\\casey\\PycharmProjects\\email_sort\\")
from secrats import ColinGTK
import google_email_pull

# Define constants for paths

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

debug_collection = debugDB['debug']
debug_id = str(uuid.uuid4())
debug_filter = {"debug_id": debug_id}
debug_collection.insert_one(debug_filter)
app = Flask(__name__)
CORS(app)  # Enable CORS for the Flask app

@app.route('/api/refresh-emails', methods=['GET'])
def refresh_emails():
    try:
        google_email_pull.get_emails()
        return jsonify({'message': 'Emails refreshed successfully.'}), 200
    except Exception as e:
        return jsonify({'error': f'Failed to refresh emails: {str(e)}'}), 500

#Gather emails from the database
@app.route('/api/get-emails', methods=['GET'])
def get_emails():
    user_sorted_emails = list(user_sorted_collection.find())
    user_unsorted_emails = list(user_collection.find())
    bot_sorted_emails = list(bot_sorted_collection.find())
    debug_collection.update_one(debug_filter, {'$set': {'emails': user_sorted_emails}})
    

    return json_util.dumps({'user_sorted_emails':user_sorted_emails, 'user_unsorted_emails': user_unsorted_emails, 'bot_sorted_emails': bot_sorted_emails}), 200

@app.route('/api/move-email', methods=['POST'])
def update_email():
    data = request.get_json()
    email_id = ObjectId(data['email']['_id'])

    # Insert the updated email into the body collection
    try:
        filter = { '_id': email_id }
        update = { '$set': { f"completion": data['email']['completion'] } }
        unsorted_email = user_collection.find_one(filter)
        user_sorted_collection.insert_one(unsorted_email)
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

    # Delete the email from the database
    try:
        unsorted_collection_db.delete_one({'_id': email_id})
    except Exception as e:
        print(f"Error deleting email: {e}")
        return jsonify({'error': f'Failed to delete email: {str(e)}'}), 500

    return jsonify({'message': 'Email deleted successfully.'}), 200
if __name__ == '__main__':
    app.run(port=config.getint('app', 'port'))
