from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from base64 import b64encode, b64decode
from os import urandom
import uuid


def encrypt(message: str, key: bytes) -> tuple[str, str]:
    iv = rand_iv()

    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())

    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(message) + encryptor.finalize()

    return b64encode(iv).decode('utf-8'), b64encode(ciphertext).decode('utf-8')


def decrypt(iv: str, ciphertext: str, key: str) -> str:
    iv = b64decode(iv)
    ciphertext = b64decode(ciphertext)

    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())

    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(ciphertext) + decryptor.finalize()

    return decrypted_message.decode('utf-8')


def rand_key() -> str:
    return urandom(32)  # 256-bit key for AES-256


def rand_iv() -> str:
    return urandom(16)


def gen_uuid() -> str:
    return str(uuid.uuid4())


if __name__ == "__main__":
    key = rand_key()
    message = "Hello, AES-256 encryption and decryption!"

    iv, ciphertext = encrypt(message.encode('utf-8'), key)
    print(f"IV: {iv}")
    print(f"Ciphertext: {ciphertext}")

    decrypted_message = decrypt(iv, ciphertext, key)
    print(f"Decrypted Message: {decrypted_message}")