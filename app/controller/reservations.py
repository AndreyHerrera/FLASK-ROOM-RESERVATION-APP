from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from boto3.dynamodb.conditions import Key
import uuid

from app.database.db import generate_dbresource

RESERVATION = Blueprint('RESERVATION', __name__)


@RESERVATION.route('/makeReservation', methods=['POST'])
def make_reservation():
    try:
        dynamodb = generate_dbresource()
        table = dynamodb.Table('reservation')
        data = request.get_json()

        if ('date' or 'time' or 'user') not in data:
            return 'Parameters are missing', 400

        reservation_id = str(uuid.uuid4())
        date = data['date']
        user = data['user']
        time = data['time']

        table.put_item(
            Item={
                'id': reservation_id,
                'date': date,
                'time': time,
                'user': user,
                'status': 'active'
            }
        )
        return 'Reservation created successfully', 201

    except Exception as e:
        return str(e), 500


@RESERVATION.route('/getReservation', methods=['GET'])
def get_reservation():
    try:
        dynamodb = generate_dbresource()
        table = dynamodb.Table('reservation')
        today = datetime.now().strftime("%d/%m/%Y")
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")

        data = request.get_json()

        if 'user' not in data:
            return 'Parameters are missing', 400

        user = data['user']
        response_table = table.scan(
            FilterExpression=Key('date').eq(today) | Key(
                'date').eq(tomorrow) & Key('status').eq('active') & Key('user').eq(user)
        )

        items = response_table['Items']
        return jsonify(items), 200

    except Exception as e:
        return str(e), 500


@RESERVATION.route('/cancelReservation', methods=['PUT'])
def cancel_reservation():
    try:
        dynamodb = generate_dbresource()
        table = dynamodb.Table('reservation')
        data = request.get_json()

        if ('date' or 'time' or 'user') not in data:
            return 'Parameters are missing', 400

        date = data['date']
        user = data['user']
        time = data['time']

        response_table = table.scan(
            FilterExpression=Key('date').eq(date) & Key(
                'time').eq(time) & Key('user').eq(user)
        )
        items = response_table['Items']

        if not items:
            return 'Reservation not found', 404

        for item in items:
            table.update_item(
                Key={'id': item['id']},
                UpdateExpression='SET #status = :status',
                ExpressionAttributeNames={'#status': 'status'},
                ExpressionAttributeValues={':status': 'canceled'}
            )

        return 'Reservation successfully canceled', 200

    except Exception as e:
        return str(e), 500
