from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mydatabase'
mongo = PyMongo(app)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8083', debug=True)
