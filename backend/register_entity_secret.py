import httpx
import os
from dotenv import load_dotenv
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
import base64
import json

load_dotenv()

API_KEY = os.getenv("CIRCLE_API_KEY")
ENTITY_SECRET = os.getenv("ENTITY_SECRET")

# Step 1: Get Circle's public key
response = httpx.get(
    "https://api.circle.com/v1/w3s/config/entity/publicKey",
    headers={"Authorization": f"Bearer {API_KEY}"}
)
print("Public key response:", response.json())
public_key_pem = response.json()["data"]["publicKey"]

# Step 2: Encrypt entity secret with Circle's public key
public_key = serialization.load_pem_public_key(
    public_key_pem.encode(),
    backend=default_backend()
)

entity_secret_bytes = bytes.fromhex(ENTITY_SECRET)

encrypted = public_key.encrypt(
    entity_secret_bytes,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

entity_secret_ciphertext = base64.b64encode(encrypted).decode()
print("\nEntity Secret Ciphertext:")
print(entity_secret_ciphertext)

# Step 3: Register with Circle
register_response = httpx.post(
    "https://api.circle.com/v1/w3s/config/entity/secretCiphertext",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    },
    json={"entitySecretCiphertext": entity_secret_ciphertext}
)
print("\nRegister response:", register_response.json())

# Save ciphertext to .env hint
print("\nAdd this to your .env:")
print(f"ENTITY_SECRET_CIPHERTEXT={entity_secret_ciphertext}")