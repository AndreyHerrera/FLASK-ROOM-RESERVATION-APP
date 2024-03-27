import datetime
from flask import app, jsonify, request
from server import mongo


@app.route('/reserve', methods=['POST'])
def reserve_room():
    data = request.json
    if data:
        room = data.get('room')
        date_str = data.get('date')
        time_str = data.get('time')

        try:
            datetime_obj = datetime.strptime(
                date_str + ' ' + time_str, '%Y-%m-%d %H:%M')
            current_time = datetime.now()
            if datetime_obj < current_time:
                return jsonify({"error": "No puedes reservar en el pasado"}), 400
        except ValueError:
            return jsonify({"error": "Formato de fecha/hora incorrecto. Usa YYYY-MM-DD HH:MM"}), 400

        inserted = mongo.db.reservations.insert_one(data)
        return jsonify({"message": "Reserva creada exitosamente", "id": str(inserted.inserted_id)}), 201
    else:
        return jsonify({"error": "Datos incorrectos"}), 400
