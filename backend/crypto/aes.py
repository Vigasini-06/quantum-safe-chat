import os
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def derive_aes_key(shared_secret):
    """
    Convert the ML-KEM shared secret into a 256-bit AES key.
    """
    return hashlib.sha256(shared_secret).digest()


def encrypt_message(message, shared_secret):
    """
    Encrypt a message using AES-256-GCM.
    """
    key = derive_aes_key(shared_secret)
    aes = AESGCM(key)

    nonce = os.urandom(12)

    encrypted = aes.encrypt(
        nonce,
        message.encode("utf-8"),
        None
    )

    return nonce, encrypted


def decrypt_message(nonce, encrypted_message, shared_secret):
    """
    Decrypt an AES-256-GCM encrypted message.
    """
    key = derive_aes_key(shared_secret)
    aes = AESGCM(key)

    decrypted = aes.decrypt(
        nonce,
        encrypted_message,
        None
    )

    return decrypted.decode("utf-8")