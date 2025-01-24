import base64

def encode_base16(text):
    return base64.b16encode(text.encode()).decode()

def decode_base16(encoded_text):
    return base64.b16decode(encoded_text).decode()