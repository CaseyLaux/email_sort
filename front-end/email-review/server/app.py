from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import shutil
import configparser
import unsorted_indexer

# Read settings from a configuration file
config = configparser.ConfigParser()
config.read('config.ini')
app_port = config.getint('app', 'port')

app = Flask(__name__)
CORS(app)  # Enable CORS for the Flask app

@app.route('/api/move-email', methods=['POST'])
def move_email():
    data = request.get_json()
    
    # Use os.path.join to build platform-independent paths
    original_path = os.path.join('..', 'public', data['originalPath'])
    new_path = os.path.join('..', 'public', data['newPath'])

    if not os.path.exists(original_path):
        return jsonify({'error': 'Source file not found.'}), 400

    try:
        shutil.move(original_path, new_path)
    except Exception as e:
        print(f"Error moving file: {e}")
        # Return a more specific error message
        return jsonify({'error': f'Failed to move email: {str(e)}'}), 500
    
    try:
        unsorted_indexer.index_emails
    except Exception as e:
        with open("debug.txt", "w") as f:
            f.write(e)
    finally:
        unsorted_indexer.index_emails()
        return jsonify({'message': 'Email moved successfully.'}), 200

if __name__ == '__main__':
    app.run(port=app_port)
