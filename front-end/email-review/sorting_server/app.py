from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import shutil
import configparser
import email_indexer
import json
from pymongo import MongoClient

# Read settings from a configuration file
config = configparser.ConfigParser()
config.read('config.ini')
app_port = config.getint('app', 'port')
mongo_uri = config.get('mongo', 'uri')  # Get MongoDB connection URI from the config file
database_name = config.get('mongo', 'database')  # Get MongoDB database name from the config file
body_collection = config.get('mongo', 'body_collection')  # Get MongoDB collection name from the config file
bodyless_collection = config.get('mongo', 'bodyless_collection')  # Get MongoDB collection name from the config file

client = MongoClient(mongo_uri)
db = client[database_name]
body_collection_db = db[body_collection]
bodyless_collection_db = db[bodyless_collection]

app = Flask(__name__)
CORS(app)  # Enable CORS for the Flask app

@app.route('/api/move-email', methods=['POST'])
def move_email():
    data = request.get_json()
    
    # Use os.path.join to build platform-independent paths
    original_path = os.path.join('..', 'public', data['originalPath'])
    new_path = os.path.join('..', 'public', data['newPath'])
    bodyless_path = os.path.join('..', 'public', data['new_bodyless_Path'])

    if not os.path.exists(original_path):
        return jsonify({'error': 'Source file not found.'}), 400

    # Move the email
    try:
        shutil.move(original_path, new_path)
    except Exception as e:
        print(f"Error moving file: {e}")
        return jsonify({'error': f'Failed to move email: {str(e)}'}), 500

    # Save the updated email JSON
    try:
        # Insert data to MongoDB
        body_collection_db.insert_one(data['email'])
        bodyless_collection_db.insert_one(data['bodyless_email'])
    except Exception as e:
        print(f"Error saving email: {e}")
        return jsonify({'error': f'Failed to save email: {str(e)}'}), 500
    
    try:
        email_indexer.index_emails()
    except Exception as e:
        print(f"Error indexing emails: {e}")

    finally:
        email_indexer.index_emails()
        return jsonify({'message': 'Email moved successfully.'}), 200

@app.route('/api/delete-email', methods=['POST'])
def delete_email():
    data = request.get_json()
    
    # Use os.path.join to build platform-independent paths
    original_path = os.path.join('..', 'public', data['originalPath'])

    if not os.path.exists(original_path):
        return jsonify({'error': 'Source file not found.'}), 400

    # Delete the email
    try:
        os.remove(original_path)
    except Exception as e:
        print(f"Error deleting file: {e}")
        return jsonify({'error': f'Failed to delete email: {str(e)}'}), 500
    
    try:
        email_indexer.index_emails()
    except Exception as e:
        print(f"Error indexing emails: {e}")

    finally:
        email_indexer.index_emails()
        return jsonify({'message': 'Email deleted successfully.'}), 200



if __name__ == '__main__':
    app.run(port=app_port)
