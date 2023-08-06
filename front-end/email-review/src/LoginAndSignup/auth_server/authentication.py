from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from flask_cors import CORS
from cerberus import Validator
import datetime
import pymongo
import hashlib

#Setup
app = Flask(__name__)
CORS(app) 
app_port = 8081
app.config['JWT_SECRET_KEY'] = '2a56363f-1c5a-434c-bd23-a8b157383ce9'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1) # define the life span of the token
jwt = JWTManager(app) # initialize JWTManager

# Specify the host and port for the MongoDB server
db_host = 'localhost'  # Replace with your MongoDB server host
db_port = 27017  # Replace with the desired port number

#MongoDB Setup
client = pymongo.MongoClient(db_host, db_port)
db = client["ai"]
users_collection = db["users"]

#Landing Page
@app.route('/')
def home():
	return 'Authorization Landing Page'

@app.route("/api/v1/auth-check", methods=["POST"])
@jwt_required()
def verify_token():
    # Getting the username from JWT token
    current_user = get_jwt_identity() # get jwt identity
    # Returning the username
    return jsonify(username=current_user), 200

#User Account Creation
@app.route("/api/v1/users", methods=["POST"])
def register():
    new_user = request.get_json() # store the json body request

    # Define a schema for our expected input
    schema = {
        'username': {'type': 'string', 'minlength': 1, 'maxlength' : 20}, 
        'email': {'type': 'string', 'minlength': 1, 'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', 'maxlength' : 60}, 
        'password': {'type': 'string', 'minlength': 1, 'maxlength' : 60}
    }
    v = Validator(schema)
    

    # Validate the input data. If it's valid, continue processing. If not, return an error message.
    if not v.validate(new_user):
        return jsonify({"msg": v.errors}), 400

    new_user["password"] = hashlib.sha256(new_user["password"].encode("utf-8")).hexdigest() 
    new_user["new_user"] = 1
    doc = users_collection.find_one({"username": new_user["username"]}) 

    if not doc:
        users_collection.insert_one(new_user)
        new_user_database = client[new_user["username"]]
        user_accounts_collection = new_user_database["email_accounts"]
        user_account_info_collection = new_user_database["acc_info"]
        user_account_info_collection.insert_one(new_user)
        
        user_accounts_collection.insert_one({"email": new_user["email"]})
        return jsonify({'msg': 'User created successfully'}), 201
    else:
        return jsonify({'msg': 'Username already exists'}), 409
    
#User Account Authentication
@app.route("/api/v1/login", methods=["POST"])
def login():
    login_details = request.get_json()

    # define a schema for our expected input
    schema = {'username': {'type': 'string', 'minlength': 1, 'maxlength': 20}, 'password': {'type': 'string', 'minlength': 1, 'maxlength': 60}}
    v = Validator(schema)

    # Validate the input data. If it's valid, continue processing. If not, return an error message.
    if not v.validate(login_details):
        return jsonify({"msg": v.errors}), 400

    username = login_details.get('username')
    password = login_details.get('password')

    user_from_db = users_collection.find_one({'username': username})

    if user_from_db:
        encrpted_password = hashlib.sha256(password.encode("utf-8")).hexdigest()
        if encrpted_password == user_from_db['password']:
            access_token = create_access_token(identity=user_from_db['username'])
            return jsonify(access_token=access_token), 200
        else:
            return jsonify({'msg': 'The username or password is incorrect'}), 401

if __name__ == '__main__':
    app.run(port=app_port)