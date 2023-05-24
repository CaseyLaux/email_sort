import base64

def encode_base64(string):
    encoded_bytes = base64.b64encode(string.encode('utf-8'))
    encoded_string = encoded_bytes.decode('utf-8')
    return encoded_string

def decode_base64(encoded_string):
    decoded_bytes = base64.b64decode(encoded_string.encode('utf-8'))
    decoded_string = decoded_bytes.decode('utf-8')
    return decoded_string

# Example usage
string_to_encode = "Hello, World!"
encoded_string = encode_base64(string_to_encode)
print("Encoded string:", encoded_string)

decoded_string = decode_base64(encoded_string)
print("Decoded string:", decoded_string)