from pqcrypto.sign import ml_dsa_65


def generate_signature_keys():
    """
    Generate an ML-DSA-65 key pair.
    """
    public_key, secret_key = ml_dsa_65.generate_keypair()
    return public_key, secret_key


def sign_message(message, secret_key):
    """
    Create an ML-DSA-65 digital signature.
    """
    signature = ml_dsa_65.sign(
        secret_key,
        message.encode("utf-8")
    )

    return signature


def verify_signature(message, signature, public_key):
    """
    Verify an ML-DSA-65 digital signature.
    """
    try:
        ml_dsa_65.verify(
            public_key,
            message.encode("utf-8"),
            signature
        )

        return True

    except Exception:
        return False