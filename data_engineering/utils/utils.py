import base64


def encode(text):
    encoded_text = text.encode('utf-8')[:6]
    return base64.b64encode(encoded_text).decode("utf-8")
