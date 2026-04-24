import httpx
import os
from dotenv import load_dotenv
import uuid

load_dotenv()

API_KEY = os.getenv("CIRCLE_API_KEY")
BASE_URL = "https://api.circle.com/v1/w3s"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def create_wallet_set():
    response = httpx.post(
        f"{BASE_URL}/developer/walletSets",
        headers=headers,
        json={
            "idempotencyKey": str(uuid.uuid4()),
            "name": "SkillBid Agents"
        }
    )
    print("Wallet Set Response:", response.json())
    return response.json()

result = create_wallet_set()
print(result)