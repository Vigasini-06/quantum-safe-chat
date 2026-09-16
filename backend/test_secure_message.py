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


# ============================================================
# ALICE AND BOB SETUP
# ============================================================

print("=== QUANTUM-SAFE CHAT TEST ===\n")


# Bob creates his ML-KEM keys
bob_kem_public, bob_kem_secret = generate_kem_keys()

# Alice creates her ML-DSA signing keys
alice_sign_public, alice_sign_secret = generate_signature_keys()


# ============================================================
# 1. ML-KEM KEY ESTABLISHMENT
# ============================================================

print("1. Establishing shared secret using ML-KEM-768...")

kem_ciphertext, alice_shared_secret = encapsulate(
    bob_kem_public
)

bob_shared_secret = decapsulate(
    bob_kem_secret,
    kem_ciphertext
)

if alice_shared_secret == bob_shared_secret:
    print("   ✓ Shared secrets match")
else:
    print("   ✗ Shared secrets do not match")


# ============================================================
# 2. ALICE CREATES MESSAGE
# ============================================================

message = "Hello Bob! This is a quantum-safe message."

print("\n2. Original message:")
print("   ", message)


# ============================================================
# 3. AES-256-GCM ENCRYPTION
# ============================================================

print("\n3. Encrypting message with AES-256-GCM...")

nonce, encrypted_message = encrypt_message(
    message,
    alice_shared_secret
)

print("   ✓ Message encrypted")


# ============================================================
# 4. ML-DSA DIGITAL SIGNATURE
# ============================================================

print("\n4. Signing message using ML-DSA-65...")

signature = sign_message(
    message,
    alice_sign_secret
)

print("   ✓ Message signed")
print("   Signature size:", len(signature), "bytes")


# ============================================================
# 5. BOB DECRYPTS MESSAGE
# ============================================================

print("\n5. Bob decrypts the message...")

decrypted_message = decrypt_message(
    nonce,
    encrypted_message,
    bob_shared_secret
)

print("   Decrypted message:")
print("   ", decrypted_message)


# ============================================================
# 6. BOB VERIFIES SIGNATURE
# ============================================================

print("\n6. Bob verifies ML-DSA-65 signature...")

signature_valid = verify_signature(
    decrypted_message,
    signature,
    alice_sign_public
)

print("   Signature valid:", signature_valid)


# ============================================================
# FINAL RESULT
# ============================================================

print("\n======================================")

if (
    alice_shared_secret == bob_shared_secret
    and message == decrypted_message
    and signature_valid
):
    print("SUCCESS!")
    print("ML-KEM-768 + AES-256-GCM + ML-DSA-65")
    print("secure message test passed.")
else:
    print("TEST FAILED.")

print("======================================")