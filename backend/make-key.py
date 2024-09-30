from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import base64
import json

# Generate private key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

# Serialize private key to PEM format
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption()
)

# Generate public key
public_key = private_key.public_key()

# Serialize public key to PEM format
public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Save keys to files
with open("private_key.pem", "wb") as private_file:
    private_file.write(private_pem)

with open("public_key.pem", "wb") as public_file:
    public_file.write(public_pem)

# Create a token (payload)
payload = {"user_id": "123", "role": "admin"}
payload_json = json.dumps(payload).encode('utf-8')

# Sign the token
signature = private_key.sign(
    payload_json,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

# Encode payload and signature in base64
encoded_payload = base64.urlsafe_b64encode(payload_json).decode('utf-8')
encoded_signature = base64.urlsafe_b64encode(signature).decode('utf-8')

# Combined token
token = f"{encoded_payload}.{encoded_signature}"

# Save the token to a file
with open("token.txt", "w") as token_file:
    token_file.write(token)

print(token)