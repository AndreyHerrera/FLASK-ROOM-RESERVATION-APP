from datetime import datetime
from app import db


class Reservation(db.Document):
    room = db.StringField(required=True)
    date = db.DateTimeField(required=True)
    time = db.StringField(required=True)
