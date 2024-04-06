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


@RESERVATION.route('/getReservation', methods=['POST'])
def get_reservation():
    try:
        dynamodb = generate_dbresource()
        table = dynamodb.Table('reservation')
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")
        day_next_tomorrow = (
            datetime.now() + timedelta(days=2)).strftime("%d/%m/%Y")

        data = request.get_json()
        items = []

        if 'user' not in data:
            return 'Parameters are missing', 400

        user = data['user']
        response_table_user = table.scan(
            FilterExpression=(Key('date').eq(day_next_tomorrow) | Key(
                'date').eq(tomorrow)) & Key('user').eq(user)
        )

        response_table_tomorrow = table.scan(
            FilterExpression=Key(
                'date').eq(tomorrow) & Key('status').eq('active'),
            ProjectionExpression='#T',  # Utilizamos un alias para el atributo 'time'
            ExpressionAttributeNames={'#T': 'time'}
        )
        response_table_next_tomorrow = table.scan(
            FilterExpression=Key('date').eq(
                day_next_tomorrow) & Key('status').eq('active'),
            ProjectionExpression='#T',  # Utilizamos un alias para el atributo 'time'
            ExpressionAttributeNames={'#T': 'time'}
        )

        items.append(response_table_user['Items'])
        items.append(response_table_tomorrow['Items'])
        items.append(response_table_next_tomorrow['Items'])
        return jsonify(items), 200

    except Exception as e:
        print(e)
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

        return {'status': True}, 201

    except Exception as e:
        print(e)
        return str(e), 500
