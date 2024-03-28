
from flask import Blueprint, app, request

from app.database.db import generate_dbresource

RESERVATION = Blueprint('RESERVATION', __name__)


@RESERVATION.route('/make_reservation', methods=['POST'])
def crear_reserva():
    dynamodb = generate_dbresource()
    table = dynamodb.Table('reservation')
    data = request.get_json()
    room_number = data['room_number']
    date = data['date']
    time = data['time']

    if room_number is None or date is None or time is None:
        return 'Faltan parámetros', 400

    try:
        table.put_item(
            Item={
                'room_number': room_number,
                'date': date,
                'time': time
            }
        )
        return 'Reserva creada exitosamente', 201

    except Exception as e:
        return str(e), 500
