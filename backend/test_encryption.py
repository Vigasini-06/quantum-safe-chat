from crypto.pqc import generate_kem_keys, encapsulate, decapsulate
from crypto.aes import encrypt_message, decrypt_message


# Bob generates his ML-KEM key pair
public_key, secret_key = generate_kem_keys()

# Alice establishes a shared secret with Bob
ciphertext, alice_secret = encapsulate(public_key)

# Bob obtains the same shared secret
bob_secret = decapsulate(secret_key, ciphertext)


# Alice encrypts a message
message = "Hello Bob! This message is quantum-safe."

nonce, encrypted_message = encrypt_message(
    message,
    alice_secret
)


# Bob decrypts the message
decrypted_message = decrypt_message(
    nonce,
    encrypted_message,
    bob_secret
)


print("Original message:")
print(message)

print("\nEncrypted message:")
print(encrypted_message.hex())

print("\nDecrypted message:")
print(decrypted_message)


if message == decrypted_message:
    print("\nSUCCESS: ML-KEM + AES-256-GCM encryption works!")
else:
    print("\nERROR: Decrypted message does not match!")