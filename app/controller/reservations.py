
from flask import Blueprint, app, request

from app.database.db import generate_dbresource

RESERVATION = Blueprint('RESERVATION', __name__)


@RESERVATION.route('/makeReservation', methods=['POST'])
def crear_reserva():
    try:
        dynamodb = generate_dbresource()
        table = dynamodb.Table('reservation')
        data = request.get_json()
        print(data)

        if ('room_number' or 'date' or 'time') not in data:
            return 'Faltan parámetros', 400

        room_number = data['room_number']
        print(room_number)
        date = data['date']
        print(date)
        time = data['time']
        print(time)

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
