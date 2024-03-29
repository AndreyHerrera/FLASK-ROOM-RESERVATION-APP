from flask import Blueprint, request
import uuid

from app.database.db import generate_dbresource

USER = Blueprint('USER', __name__)


@USER.route('/registerUser', methods=['POST'])
def register_user():
    try:
        dynamodb = generate_dbresource()
        table = dynamodb.Table('user')
        data = request.get_json()

        if ('email' or 'password') not in data:
            return 'Parameters are missing', 400

        user_id = str(uuid.uuid4())
        email = data['email']
        password = data['password']

        table.put_item(
            Item={
                'id': user_id,
                'email': email,
                'password': password,
            }
        )
        return 'User created successfully', 201

    except Exception as e:
        return str(e), 500


@USER.route('/loginUser', methods=['POST'])
def login_user():
    pass


def generate_jwt():
    pass
