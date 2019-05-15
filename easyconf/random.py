import base64
import math
import os


def random_text_generator(length: int):
    b64_len = math.ceil(length / 4 * 3)

    def generate():
        return base64.b64encode(os.urandom(b64_len)).decode()[:length]

    return generate
