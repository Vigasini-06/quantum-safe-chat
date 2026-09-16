from crypto.signatures import (
    generate_signature_keys,
    sign_message,
    verify_signature
)


# Alice generates her ML-DSA-65 key pair
public_key, secret_key = generate_signature_keys()

# Alice creates a message
message = "Hello Bob! This message is digitally signed."

# Alice signs the message
signature = sign_message(message, secret_key)

# Bob verifies the signature
valid = verify_signature(
    message,
    signature,
    public_key
)

print("Message:")
print(message)

print("\nSignature length:")
print(len(signature), "bytes")

print("\nSignature valid:")
print(valid)

if valid:
    print("\nSUCCESS: ML-DSA-65 signature verified!")
else:
    print("\nERROR: Signature verification failed!")