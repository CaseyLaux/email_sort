from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import shutil
import configparser
from pymongo import MongoClient
import email_indexer

# Define constants for paths
BASE_PATH = os.path.join('..', 'public')

# Read settings from a configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Get MongoDB settings from the config file
mongo_settings = {key: config.get('mongo', key) for key in ['uri', 'database', 'body_collection', 'bodyless_collection']}

# Get MongoDB connection and collections
client = MongoClient(mongo_settings['uri'])
db = client[mongo_settings['database']]
body_collection_db = db[mongo_settings['body_collection']]
bodyless_collection_db = db[mongo_settings['bodyless_collection']]

app = Flask(__name__)
CORS(app)  # Enable CORS for the Flask app

def handle_email_move(original_path, new_path, email_data):
    # Move the email
    try:
        shutil.move(original_path, new_path)
        # Insert data to MongoDB
        body_collection_db.insert_one(email_data['email'])
        bodyless_collection_db.insert_one(email_data['bodyless_email'])
    except Exception as e:
        print(f"Error moving or saving email: {e}")
        return jsonify({'error': f'Failed to move or save email: {str(e)}'}), 500

@app.route('/api/move-email', methods=['POST'])
def move_email():
    data = request.get_json()
    original_path = os.path.join(BASE_PATH, data['originalPath'])
    new_path = os.path.join(BASE_PATH, data['newPath'])

    if not os.path.exists(original_path):
        return jsonify({'error': 'Source file not found.'}), 400

    response = handle_email_move(original_path, new_path, data)
    email_indexer.index_emails()
    return response if response else jsonify({'message': 'Email moved successfully.'}), 200

@app.route('/api/delete-email', methods=['POST'])
def delete_email():
    data = request.get_json()
    original_path = os.path.join(BASE_PATH, data['originalPath'])

    if not os.path.exists(original_path):
        return jsonify({'error': 'Source file not found.'}), 400

    # Delete the email
    try:
        os.remove(original_path)
    except Exception as e:
        print(f"Error deleting file: {e}")
        return jsonify({'error': f'Failed to delete email: {str(e)}'}), 500

    email_indexer.index_emails()
    return jsonify({'message': 'Email deleted successfully.'}), 200

if __name__ == '__main__':
    app.run(port=config.getint('app', 'port'))
