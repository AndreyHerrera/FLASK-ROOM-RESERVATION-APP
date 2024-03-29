import jwt

KEY_ENCRIPT = "WOLFANGHERRERA"


def generate_jwt(email, date):
    payload = {
        'email': email,
        'exp': date
    }
    key = KEY_ENCRIPT

    return jwt.encode(payload, key, algorithm='HS256')
