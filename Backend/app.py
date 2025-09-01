from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
import datetime

app = Flask(__name__)
CORS(app)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/ths_db'  # Change as needed
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change for production
mongo = PyMongo(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# User registration (for admin/setup only)
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if mongo.db.users.find_one({'username': username}):
        return jsonify({'msg': 'User already exists'}), 409
    pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    mongo.db.users.insert_one({'username': username, 'password': pw_hash})
    return jsonify({'msg': 'User registered'}), 201

# User login
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = mongo.db.users.find_one({'username': data.get('username')})
    if user and bcrypt.check_password_hash(user['password'], data.get('password')):
        access_token = create_access_token(identity=user['username'], expires_delta=datetime.timedelta(days=1))
        return jsonify(access_token=access_token), 200
    return jsonify({'msg': 'Invalid credentials'}), 401

# Get catalog
@app.route('/api/catalog', methods=['GET'])
@jwt_required()
def get_catalog():
    items = list(mongo.db.catalog.find({}, {'_id': 0}))
    return jsonify(items)

# Create quotation
@app.route('/api/quotation', methods=['POST'])
@jwt_required()
def create_quotation():
    data = request.get_json()
    user = get_jwt_identity()
    quotation = {
        'user': user,
        'items': data.get('items', []),
        'notes': data.get('notes', ''),
        'created_at': datetime.datetime.utcnow()
    }
    mongo.db.quotations.insert_one(quotation)
    return jsonify({'msg': 'Quotation created'}), 201

# Get user quotations
@app.route('/api/quotation', methods=['GET'])
@jwt_required()
def get_quotations():
    user = get_jwt_identity()
    quotations = list(mongo.db.quotations.find({'user': user}, {'_id': 0}))
    return jsonify(quotations)

if __name__ == '__main__':
    app.run(debug=True)
