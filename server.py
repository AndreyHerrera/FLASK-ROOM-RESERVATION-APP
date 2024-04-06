from flask import Flask
from flask_cors import CORS

from app.controller.reservations import RESERVATION
from app.controller.user import USER

APP = Flask(__name__)
APP.register_blueprint(RESERVATION)
APP.register_blueprint(USER)
CORS(APP, origins='http://localhost:4200', methods=['POST', 'PUT', 'DELETE'])


if __name__ == "__main__":
    APP.run(host='0.0.0.0', port='8083', debug=True)
