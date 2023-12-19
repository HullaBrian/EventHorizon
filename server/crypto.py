# server/crypto.py
import random
import string
import sys
import traceback
import uuid

from base64 import b64encode, b64decode
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from os import urandom


def encrypt(message: str, iv: bytes, key: bytes) -> tuple[str]:
    """
    Encrypt a message using AES-256-CTR
    Returns the cipher text in byte form
    """
    cipher = Cipher(algorithms.AES256(key), modes.CTR(iv), backend=default_backend())

    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(message) + encryptor.finalize()

    # return b64encode(iv).decode('utf-8'), b64encode(ciphertext).decode('utf-8')
    return ciphertext


def decrypt(iv: bytes, ciphertext: bytes, key: bytes) -> bytes:
    """
    Decrypt ciphertext using AES-256-CTR
    Returns bytes representing the decrypted message
    """
    cipher = Cipher(algorithms.AES(key), modes.CTR(iv), backend=default_backend())

    decryptor = cipher.decryptor()
    try:
        decrypted_message = decryptor.update(ciphertext)  # + decryptor.finalize()
    except ValueError as e:
        traceback.print_exc()
        sys.exit()
    except UnicodeDecodeError:
        return "UNKNOWN!"
    
    return decrypted_message


def rand_key() -> bytes:
    """
    Generate a random key for use in AES-256-CTR encryption
    """
    return urandom(32)


def rand_iv() -> bytes:
    """
    Generate a initialization vector for use in AES-256-CTR encryption
    """
    return urandom(16)


def gen_uuid() -> str:
    """
    generates a 32 character long uuid
    32 characters long to not have to add padding during agent hello message
    """ 
    return str(uuid.uuid4()).ljust(32)[:32].replace(" ", "-")


if __name__ == "__main__":
    key = b've3wwzT9auRC9vYk/1CqNARPFZuzTExx'
    iv = b'3jBjd4Puv32Fk0e/'
    message = "CAHZJJjEwXnaCqUNhjhwZWrWwLhiAhfM"

    ciphertext = encrypt(message.encode('utf-8'), iv, key)
    print(f"Message: {message}")
    print(f"Key: {key}")
    print(f"IV: {iv}")
    print(f"Ciphertext: {ciphertext}")

    decrypted_message = decrypt(iv, ciphertext, key)
    print(f"Decrypted Message: {decrypted_message}")
