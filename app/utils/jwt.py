from datetime import datetime, timedelta
import jwt

KEY_ENCRIPT = "WOLFANGHERRERA"


def encode_jwt(email, date):
    payload = {
        'email': email,
        'exp': datetime.utcnow() + timedelta(minutes=1)
    }
    key = KEY_ENCRIPT

    return jwt.encode(payload, key, algorithm='HS256')


def decode_jwt(token):
    try:
        key = KEY_ENCRIPT
        payload = jwt.decode(token, key, algorithms=['HS256'])
        expiration = datetime.utcfromtimestamp(
            payload['exp']).replace(tzinfo=None)
        now = datetime.utcnow()
        if expiration > now:
            return True
        else:
            return False
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False
