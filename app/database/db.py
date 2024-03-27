from server import mongo


def create_collection_if_not_exists():
    if 'reservations' not in mongo.db.list_collection_names():
        mongo.db.create_collection('reservations')
