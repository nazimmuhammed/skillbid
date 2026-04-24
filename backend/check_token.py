import httpx
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("CIRCLE_API_KEY")

response = httpx.get(
    "https://api.circle.com/v1/w3s/wallets/04df4124-f2de-5c86-ba57-739654b885b2/balances",
    headers={"Authorization": f"Bearer {API_KEY}"}
)
print(response.json())