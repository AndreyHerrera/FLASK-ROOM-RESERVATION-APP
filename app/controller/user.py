from flask import Blueprint, jsonify, request
import uuid
from datetime import datetime
from boto3.dynamodb.conditions import Key

from app.database.db import generate_dbresource
from app.utils.crypto import encrypt
from app.utils.jwt import decode_jwt, encode_jwt

USER = Blueprint('USER', __name__)


@USER.route('/registerUser', methods=['POST'])
def register_user():
    try:
        dynamodb = generate_dbresource()
        table_user = dynamodb.Table('user')
        data = request.get_json()

        if ('email' or 'password') not in data:
            return 'Parameters are missing', 400

        user_id = str(uuid.uuid4())
        email = data['email']
        password = encrypt(data['password'])

        table_user.put_item(
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
        table_user = dynamodb.Table('user')
        data = request.get_json()

        if ('email' or 'password') not in data:
            return 'Parameters are missing', 400

        email = data['email']
        password = encrypt(data['password'])

        response_table = table_user.scan(
            FilterExpression=Key(
                'email').eq(email) & Key('password').eq(password)
        )

        date = datetime.now().strftime('%d/%m/%Y %H:%M')
        response = {'status': False}
        if response_table['Items']:

            token = encode_jwt(email)

            response['status'] = True
            response['token'] = token

            table_session = dynamodb.Table('session')
            table_session.put_item(
                Item={
                    'token': token,
                    'email': email,
                }
            )

        return response, 200

    except Exception as e:
        return str(e), 500


@USER.route('/validateSession', methods=['POST'])
def validate_session():
    try:
        dynamodb = generate_dbresource()
        table = dynamodb.Table('session')
        data = request.get_json()

        if ('email' or 'token') not in data:
            return 'Parameters are missing', 400

        email = data['email']
        token = data['token']

        response_table = table.scan(
            FilterExpression=Key(
                'email').eq(email) & Key('token').eq(token)
        )
        if response_table['Items']:
            validated = decode_jwt(token)
            return {'status': validated}, 200

        else:
            return {'status': False}, 200

    except Exception as e:
        return str(e), 500
