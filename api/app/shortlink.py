import os
import base62

NUM_BYTES = 7
URL_LENGTH = 7

def random_url():
    return random_base62_string(NUM_BYTES)[:URL_LENGTH]

def random_base62_string(num_bytes: int) -> str:
    random_string = os.urandom(num_bytes)
    return base62.encodebytes(random_string)
