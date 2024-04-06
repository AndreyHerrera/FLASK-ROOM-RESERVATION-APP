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

        if ('user' or 'password') not in data:
            return 'Parameters are missing', 400

        user_id = str(uuid.uuid4())
        user = data['user']
        password = encrypt(data['password'])

        table_user.put_item(
            Item={
                'id': user_id,
                'user': user,
                'password': password,
            }
        )

        return {'status': True}, 201

    except Exception:
        return {'status': False}, 500


@USER.route('/loginUser', methods=['POST'])
def login_user():
    try:
        dynamodb = generate_dbresource()
        table_user = dynamodb.Table('user')
        data = request.get_json()

        if ('user' or 'password') not in data:
            return 'Parameters are missing', 400

        user = data['user']
        password = encrypt(data['password'])

        response_table = table_user.scan(
            FilterExpression=Key(
                'user').eq(user) & Key('password').eq(password)
        )

        response = {'status': False}
        if response_table['Items']:

            token = encode_jwt(user)

            response['status'] = True
            response['token'] = token

            # table_session = dynamodb.Table('session')
            # table_session.put_item(
            #     Item={
            #         'token': token,
            #         'user': user,
            #     }
            # )

        return response, 200

    except Exception:
        return response, 200


@USER.route('/validateSession', methods=['POST'])
def validate_session():
    try:
        dynamodb = generate_dbresource()
        table = dynamodb.Table('session')
        data = request.get_json()

        if ('user' or 'token') not in data:
            return 'Parameters are missing', 400

        user = data['user']
        token = data['token']

        response_table = table.scan(
            FilterExpression=Key(
                'user').eq(user) & Key('token').eq(token)
        )
        if response_table['Items']:
            validated = decode_jwt(token)
            return {'status': validated}, 200

        else:
            return {'status': False}, 200

    except Exception as e:
        return str(e), 500
