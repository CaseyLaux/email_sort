from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import shutil
import configparser
import email_indexer
import json

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

    # Move the email
    try:
        shutil.move(original_path, new_path)
    except Exception as e:
        with open("debug.txt", "w") as x:
            x.write(str(e))
            x.write(f"{original_path}, \n , {new_path}")
            x.write("failed to move email")
        print(f"Error moving file: {e}")
        return jsonify({'error': f'Failed to move email: {str(e)}'}), 500

    # Save the updated email JSON
    try:
        with open(new_path, 'w') as f:
            json.dump(data['email'], f)
         # New code: save the updatedEmail_bodyless JSON to a new file.
        with open(new_path.replace('.json', '_bodyless.json'), 'w') as f:
            json.dump(data['emails'], f)
    except Exception as e:
        with open("debug.json","w" ) as d:
            json.dump(data['email'], d)
    except Exception as e:
        with open("debug.json","w" ) as d:
            json.dump(data, d)
        with open("debug.txt", "w") as x:
            x.write(str(e))
            x.write(data['email'])
            x.write(f"${original_path}, \n , ${new_path}")
            x.write("json_dump_error")
        print(f"Error saving email: {e}")
        return jsonify({'error': f'Failed to save email: {str(e)}'}), 500
    
    try:
        os.getcwd
        email_indexer.index_emails()
    except Exception as e:
        with open("debug.txt", "w") as x:
            x.write(str(e))
            x.write("test_indexer")
            x.write(f"${original_path}, \n , ${new_path}")

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
        with open("debug.txt", "w") as x:
            x.write(str(e))
            x.write("test_indexer")
            x.write(f"{original_path}")

    finally:
        email_indexer.index_emails()
        return jsonify({'message': 'Email deleted successfully.'}), 200



if __name__ == '__main__':
    app.run(port=app_port)
