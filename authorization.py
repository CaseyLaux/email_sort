from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required

import datetime
import pymongo
import hashlib

#Setup
app = Flask(__name__)
port = 8081
jwt = JWTManager(app) # initialize JWTManager
app.config['JWT_SECRET_KEY'] = '2a56363f-1c5a-434c-bd23-a8b157383ce9'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1) # define the life span of the token

# Specify the host and port for the MongoDB server
host = 'localhost'  # Replace with your MongoDB server host
port = 27017  # Replace with the desired port number

#MongoDB Setup
client = pymongo.MongoClient(host, port)
db = client["ai"]
users_collection = db["users"]

@app.route('/')
def home():
	return 'Authorization Landing Page'


#User Account Creation
@app.route("/api/v1/users", methods=["POST"])
def register():
    new_user = request.get_json() # store the json body request
    if(new_user['username'] == None or new_user['email'] == None or new_user['password'] == None):
        return jsonify({'msg': 'Please include the correct fields!'}), 406
    # Creating Hash of password to store in the database
    new_user["password"] = hashlib.sha256(new_user["password"].encode("utf-8")).hexdigest() # encrpt password
    # Checking if user already exists
    doc = users_collection.find_one({"username": new_user["username"]}) # check if user exist
    # If not exists than create one
    if not doc:
        # Creating user
        users_collection.insert_one(new_user)
        return jsonify({'msg': 'User created successfully'}), 201
    else:
        return jsonify({'msg': 'Username already exists'}), 409
    
#User Account Authentication
@app.route("/api/v1/login", methods=["POST"])
def login():
    # Getting the login Details from payload
    login_details = request.get_json() # store the json body request
    # Checking if user exists in database or not
    user_from_db = users_collection.find_one({'username': login_details['username']})  # search for user in database
    # If user exists
    if user_from_db:
        # Check if password is correct
        encrpted_password = hashlib.sha256(login_details['password'].encode("utf-8")).hexdigest()
        if encrpted_password == user_from_db['password']:
            # Create JWT Access Token
            access_token = create_access_token(identity=user_from_db['username']) # create jwt token
            # Return Token
            return jsonify(access_token=access_token), 200
        else:
            return jsonify({'msg': 'The username or password is incorrect'}), 401

if __name__ == '__main__':
    app.run(port=port)