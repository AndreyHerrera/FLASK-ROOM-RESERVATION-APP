from flask import Blueprint, jsonify, request
import uuid
from datetime import datetime
from boto3.dynamodb.conditions import Key

from app.database.db import generate_dbresource
from app.utils.crypto import encrypt
from app.utils.jwt import generate_jwt

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
        password = encrypt(data['password'])

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
    try:
        dynamodb = generate_dbresource()
        table = dynamodb.Table('user')
        data = request.get_json()

        if ('email' or 'password') not in data:
            return 'Parameters are missing', 400

        email = data['email']
        password = encrypt(data['password'])

        response_table = table.scan(
            FilterExpression=Key(
                'email').eq(email) & Key('password').eq(password)
        )

        date = datetime.now().strftime('%d/%m/%Y %H:%M')
        response = {'status': False}
        if response_table['Items']:
            response['status'] = True
            response['token'] = generate_jwt(email, date)

        return response, 200

    except Exception as e:
        return str(e), 500
