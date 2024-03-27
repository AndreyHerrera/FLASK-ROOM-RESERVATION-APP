import datetime
from flask import app, jsonify, request
from app.database.models import Reservation
from server import mongo


@app.route('/reserve', methods=['POST'])
def create_reservation():
    data = request.get_json()
    if data:
        reservation = Reservation(
            room=data['numberRoom'], date=data['dateReservation'], time=data['timeReservation'])
        reservation.save()
        return jsonify({"message": "Reserva creada exitosamente", "id": str(reservation.id)}), 201
    else:
        return jsonify({"error": "Datos incorrectos"}), 400
