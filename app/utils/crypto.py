import base64

KEY_ENCRIPT = "WOLFANGHERRERA"


def encrypt(text):
    key = KEY_ENCRIPT

    key_bytes = key.encode('utf-8')
    key_bytes = key_bytes + b'\x00' * (32 - len(key_bytes))

    text_bytes = text.encode('utf-8')

    encrypted_text = base64.b64encode(text_bytes)

    return encrypted_text
