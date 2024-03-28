
from flask import Blueprint, app, jsonify, request
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

        if ('date' or 'time') not in data:
            return 'Parameters are missing', 400

        reservation_id = str(uuid.uuid4())
        date = data['date']
        time = data['time']

        table.put_item(
            Item={
                'id': reservation_id,
                'date': date,
                'time': time,
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

        response = table.scan(
            FilterExpression=Key('date').eq(today) | Key(
                'date').eq(tomorrow) & Key('status').eq('active')
        )

        items = response['Items']
        return jsonify(items), 200

    except Exception as e:
        return str(e), 500


@RESERVATION.route('/cancelReservation', methods=['PUT'])
def cancel_reservation():
    try:
        dynamodb = generate_dbresource()
        table = dynamodb.Table('reservation')
        data = request.get_json()

        if ('date' or 'time') not in data:
            return 'Parameters are missing', 400

        date = data['date']
        time = data['time']

        response = table.scan(
            FilterExpression=Key('date').eq(date) & Key('time').eq(time)
        )
        items = response['Items']

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
