from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus

username = quote_plus('wolfangaherrerac')
password = quote_plus('pesxiv-8wyxje-capRid')


credentials = f"mongodb+srv://{username}:{password}@roomreservations.hhwd7hh.mongodb.net/?retryWrites=true&w=majority&appName=RoomReservations"
client = MongoClient(credentials, server_api=ServerApi('1'))


def create_collection_if_not_exists():
    db = client.mydatabase
    if 'reservations' not in db.list_collection_names():
        db.create_collection('reservations')
        print("Colección 'reservations' creada.")
    else:
        print("La colección 'reservations' ya existe.")
