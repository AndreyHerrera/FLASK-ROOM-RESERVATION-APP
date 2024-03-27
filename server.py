from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

from app.database.db import create_collection_if_not_exists

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mydatabase'
mongo = PyMongo(app)


if __name__ == "__main__":
    create_collection_if_not_exists()
    app.run(host='0.0.0.0', port='8083', debug=True)
