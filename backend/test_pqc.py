from crypto.pqc import generate_kem_keys, encapsulate, decapsulate


# Generate Bob's ML-KEM key pair
public_key, secret_key = generate_kem_keys()

# Alice creates a shared secret
ciphertext, alice_secret = encapsulate(public_key)

# Bob recovers the same shared secret
bob_secret = decapsulate(secret_key, ciphertext)

print("Alice secret:", alice_secret.hex())
print("Bob secret:  ", bob_secret.hex())

if alice_secret == bob_secret:
    print("\nSUCCESS: ML-KEM shared secrets match!")
else:
    print("\nERROR: Shared secrets do not match!")