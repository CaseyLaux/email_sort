from bson import json_util, ObjectId
from flask import Flask, request, jsonify
from flask_cors import CORS
import configparser
from pymongo import MongoClient

# Define constants for paths

# Read settings from a configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Get MongoDB settings from the config file
mongo_settings = {key: config.get('mongo', key) for key in ['uri', 'database', 'body_collection', 'bodyless_collection', 'unsorted_collection']}

# Get MongoDB connection and collections
client = MongoClient(mongo_settings['uri'])
db = client[mongo_settings['database']]
body_collection_db = db[mongo_settings['body_collection']]
bodyless_collection_db = db[mongo_settings['bodyless_collection']]
unsorted_collection_db = db[mongo_settings['unsorted_collection']]
app = Flask(__name__)
CORS(app)  # Enable CORS for the Flask app

#Gather emails from the database
@app.route('/api/get-emails', methods=['GET'])
def get_emails():
    body_emails = list(body_collection_db.find())
    unsorted_emails = list(unsorted_collection_db.find())
    return json_util.dumps({'body_emails':body_emails, 'unsorted_emails': unsorted_emails}), 200
def handle_email_move(email_data):
    # Move the email
    try:
        # Insert data to MongoDB
        body_collection_db.insert_one(email_data['email'])
        bodyless_collection_db.insert_one(email_data['bodyless_email'])
    except Exception as e:
        print(f"Error moving or saving email: {e}")
        return jsonify({'error': f'Failed to move or save email: {str(e)}'}), 500
@app.route('/api/move-email', methods=['POST'])
def move_email():
    data = request.get_json()
    email_id = ObjectId(data['email']['_id'])

    # Delete the email from the unsorted collection
    

    # Insert the updated email into the body collection
    try:
        body_collection_db.insert_one(data['email'])
    except Exception as e:
        print(f"Error inserting email: {e}")
        return jsonify({'error': f'Failed to insert email: {str(e)}'}), 500
    try:
        unsorted_collection_db.delete_one({'_id': email_id})
    except Exception as e:
        print(f"Error deleting email: {e}")
        return jsonify({'error': f'Failed to delete email: {str(e)}'}), 500

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
