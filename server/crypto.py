import string
import uuid
import random
import traceback

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from base64 import b64encode, b64decode
from os import urandom


def encrypt(message: str, key: bytes) -> tuple[str, str]:
    iv = rand_iv()
    # iv = b'3jBjd4Puv32Fk0e/'

    cipher = Cipher(algorithms.AES256(key), modes.CTR(iv), backend=default_backend())

    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(message) + encryptor.finalize()

    # return b64encode(iv).decode('utf-8'), b64encode(ciphertext).decode('utf-8')
    return ciphertext


def decrypt(iv: bytes, ciphertext: bytes, key: bytes) -> str:
    cipher = Cipher(algorithms.AES(key), modes.CTR(iv), backend=default_backend())

    decryptor = cipher.decryptor()
    try:
        decrypted_message = decryptor.update(ciphertext)  # + decryptor.finalize()
    except ValueError as e:
        traceback.print_exc()
        exit()
    except UnicodeDecodeError:
        return "UNKNOWN!"
    
    return decrypted_message


def padding(buffer: str) -> str:
    out = ""
    remainder = len(buffer) % 16
    if remainder == 0:
        return buffer

    for i in range(16 - remainder):
        out += random.choice(string.ascii_letters)
    return buffer + out


def rand_key() -> str:
    return urandom(32)


def rand_iv() -> str:
    return urandom(16)


def gen_uuid() -> str:
    # generates a 32 character long uuid
    # 32 characters long to not have to add padding during agent hello message
    return str(uuid.uuid4()).ljust(32)[:32].replace(" ", "-")


if __name__ == "__main__":
    key = b've3wwzT9auRC9vYk/1CqNARPFZuzTExx'
    iv = b'3jBjd4Puv32Fk0e/'
    message = "CAHZJJjEwXnaCqUNhjhwZWrWwLhiAhfM"

    ciphertext = encrypt(message.encode('utf-8'), key)
    print(f"Message: {message}")
    print(f"Key: {key}")
    print(f"IV: {iv}")
    print(f"Ciphertext: {ciphertext}")

    decrypted_message = decrypt(iv, ciphertext, key)
    print(f"Decrypted Message: {decrypted_message}")
