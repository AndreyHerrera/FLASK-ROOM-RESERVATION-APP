from flask import Flask, request, jsonify

from app.database.db import client, create_collection_if_not_exists

app = Flask(__name__)

if __name__ == "__main__":
    client.admin.command('ping')
    create_collection_if_not_exists()
    app.run(host='0.0.0.0', port='8083', debug=True)
