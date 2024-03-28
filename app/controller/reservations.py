
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

        if ('room_number' or 'date' or 'time') not in data:
            return 'Faltan parámetros', 400

        reservation_id = str(uuid.uuid4())
        room_number = data['room_number']
        date = data['date']
        time = data['time']

        table.put_item(
            Item={
                'id': reservation_id,
                'room_number': room_number,
                'date': date,
                'time': time
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
            FilterExpression=Key('date').eq(today) | Key('date').eq(tomorrow)
        )

        items = response['Items']
        return jsonify(items), 200
    except Exception as e:
        return str(e), 500
