from server import APP


def encrypt(text):
    key = APP.config['KEY_USER']
    encrypted_text = ""
    for char in text:
        encrypted_text += chr(ord(char) + key)
    return encrypted_text


def decrypt(encrypted_text):
    key = APP.config['KEY_USER']
    decrypted_text = ""
    for char in encrypted_text:
        decrypted_text += chr(ord(char) - key)
    return decrypted_text
