import base64

def encode_base32(text):
    return base64.b32encode(text.encode()).decode()

def decode_base32(encoded_text):
    return base64.b32decode(encoded_text).decode()