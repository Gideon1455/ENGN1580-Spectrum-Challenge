import random
import socket
import threading

SIGNATURE_LENGTH = 256
CHANNEL_NAME = "XXXCDMA"
PORT = 12345
student_id = "1234567"


def encode_message(m, sig):
    encoded = [m[i] * sig[i] for i in range(SIGNATURE_LENGTH)]
    return encoded


def decode_message(received, sig):
    decoded_message = sum([received[i] * sig[i] for i in range(SIGNATURE_LENGTH)])
    decoded_message = 1 if decoded_message > 0 else -1
    return decoded_message


def generate_signature(id):
    random.seed(id)
    sig = [random.choice([1, -1]) for _ in range(SIGNATURE_LENGTH)]
    return sig


signature = generate_signature(student_id)

# messages = [
#     [-1 if i % 2 == 0 else 1 for i in range(SIGNATURE_LENGTH)],
#     [1 if i % 3 == 0 else -1 for i in range(SIGNATURE_LENGTH)],
#     [-1 if i % 4 == 0 else 1 for i in range(SIGNATURE_LENGTH)],
# ]
for message in messages:
    encoded_message = encode_message(message, signature)
    encoded_message_str = "".join([str(bit) for bit in encoded_message])
