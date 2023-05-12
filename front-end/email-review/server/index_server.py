from flask import Flask, request, jsonify
from flask_cors import CORS
import unsorted_indexer

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

@app.route('/index_emails', methods=['POST'])
def run_python_script():
    data = request.get_json()
    # Pass any required data from the request to your Python script
    unsorted_indexer.index_emails()
    result = {"message": "Script finished successfully."}
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
