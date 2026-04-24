import httpx
import os
from dotenv import load_dotenv
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
import base64
import uuid

load_dotenv()

API_KEY = os.getenv("CIRCLE_API_KEY")
ENTITY_SECRET = os.getenv("ENTITY_SECRET")

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def get_ciphertext():
    # Get Circle's public key
    response = httpx.get(
        "https://api.circle.com/v1/w3s/config/entity/publicKey",
        headers=headers
    )
    public_key_pem = response.json()["data"]["publicKey"]
    
    # Encrypt entity secret
    public_key = serialization.load_pem_public_key(
        public_key_pem.encode(),
        backend=default_backend()
    )
    encrypted = public_key.encrypt(
        bytes.fromhex(ENTITY_SECRET),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.b64encode(encrypted).decode()

# Step 1: Fresh ciphertext
print("Generating fresh ciphertext...")
ciphertext = get_ciphertext()
print("Done.")

# Step 2: Create wallet set
print("\nCreating wallet set...")
wallet_set_response = httpx.post(
    "https://api.circle.com/v1/w3s/developer/walletSets",
    headers=headers,
    json={
        "idempotencyKey": str(uuid.uuid4()),
        "name": "SkillBid Agents",
        "entitySecretCiphertext": ciphertext
    }
)
print(wallet_set_response.json())
wallet_set_id = wallet_set_response.json()["data"]["walletSet"]["id"]

# Step 3: Create 4 wallets
print("\nCreating wallets...")
ciphertext = get_ciphertext()  # Fresh ciphertext again
wallets_response = httpx.post(
    "https://api.circle.com/v1/w3s/developer/wallets",
    headers=headers,
    json={
        "idempotencyKey": str(uuid.uuid4()),
        "blockchains": ["ARB-SEPOLIA"],
        "count": 4,
        "entitySecretCiphertext": ciphertext,
        "walletSetId": wallet_set_id
    }
)
print(wallets_response.json())

agents = ["orchestrator", "summarizer", "translator", "sentiment"]
wallets = wallets_response.json()["data"]["wallets"]

print("\n===== COPY THESE TO .env =====")
for i, wallet in enumerate(wallets):
    print(f"{agents[i].upper()}_WALLET_ID={wallet['id']}")
    print(f"{agents[i].upper()}_WALLET_ADDRESS={wallet['address']}")