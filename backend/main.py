from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from crypto.pqc import (
    generate_kem_keys,
    encapsulate,
    decapsulate
)

from crypto.aes import (
    encrypt_message,
    decrypt_message
)

from crypto.signatures import (
    generate_signature_keys,
    sign_message,
    verify_signature
)


app = FastAPI(
    title="Quantum-Safe Chat API",
    description="Chat API using ML-KEM-768, AES-256-GCM and ML-DSA-65",
    version="2.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# Temporary in-memory key storage
# ============================================================

bob_kem_public = None
bob_kem_secret = None

alice_sign_public = None
alice_sign_secret = None


# ============================================================
# Request models
# ============================================================

class MessageRequest(BaseModel):
    message: str


class DecryptRequest(BaseModel):
    nonce: str
    encrypted_message: str
    kem_ciphertext: str


class VerifyRequest(BaseModel):
    message: str
    signature: str


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():
    return {
        "project": "Quantum-Safe Chat",
        "status": "running",
        "algorithms": {
            "key_exchange": "ML-KEM-768",
            "encryption": "AES-256-GCM",
            "digital_signature": "ML-DSA-65"
        }
    }


# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# ============================================================
# GENERATE KEYS
# ============================================================

@app.post("/keys/generate")
def generate_keys():
    global bob_kem_public
    global bob_kem_secret
    global alice_sign_public
    global alice_sign_secret

    bob_kem_public, bob_kem_secret = generate_kem_keys()

    alice_sign_public, alice_sign_secret = generate_signature_keys()

    return {
        "status": "success",
        "message": "ML-KEM-768 and ML-DSA-65 keys generated"
    }


# ============================================================
# ENCRYPT MESSAGE
# ============================================================

@app.post("/messages/encrypt")
def encrypt_message_api(request: MessageRequest):

    if bob_kem_public is None:
        raise HTTPException(
            status_code=400,
            detail="Generate keys first using /keys/generate"
        )

    # ML-KEM establishes shared secret
    kem_ciphertext, shared_secret = encapsulate(
        bob_kem_public
    )

    # AES-256-GCM encrypts message
    nonce, encrypted_message = encrypt_message(
        request.message,
        shared_secret
    )

    # ML-DSA signs the original message
    signature = sign_message(
        request.message,
        alice_sign_secret
    )

    return {
        "kem_ciphertext": kem_ciphertext.hex(),
        "nonce": nonce.hex(),
        "encrypted_message": encrypted_message.hex(),
        "signature": signature.hex()
    }


# ============================================================
# DECRYPT MESSAGE
# ============================================================

@app.post("/messages/decrypt")
def decrypt_message_api(request: DecryptRequest):

    if bob_kem_secret is None:
        raise HTTPException(
            status_code=400,
            detail="Generate keys first using /keys/generate"
        )

    try:

        kem_ciphertext = bytes.fromhex(
            request.kem_ciphertext
        )

        nonce = bytes.fromhex(
            request.nonce
        )

        encrypted_message = bytes.fromhex(
            request.encrypted_message
        )

        # Recover shared secret
        shared_secret = decapsulate(
            bob_kem_secret,
            kem_ciphertext
        )

        # Decrypt message
        message = decrypt_message(
            nonce,
            encrypted_message,
            shared_secret
        )

        return {
            "status": "success",
            "message": message
        }

    except Exception as error:

        raise HTTPException(
            status_code=400,
            detail=f"Decryption failed: {str(error)}"
        )


# ============================================================
# VERIFY DIGITAL SIGNATURE
# ============================================================

@app.post("/messages/verify")
def verify_message(request: VerifyRequest):

    if alice_sign_public is None:
        raise HTTPException(
            status_code=400,
            detail="Generate keys first using /keys/generate"
        )

    try:

        signature = bytes.fromhex(
            request.signature
        )

        valid = verify_signature(
            request.message,
            signature,
            alice_sign_public
        )

        return {
            "signature_valid": valid
        }

    except Exception as error:

        raise HTTPException(
            status_code=400,
            detail=f"Verification failed: {str(error)}"
        )