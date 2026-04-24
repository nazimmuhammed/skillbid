import httpx
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("CIRCLE_API_KEY")

response = httpx.get(
    "https://api.circle.com/v1/w3s/tokens?blockchain=ARB-SEPOLIA",
    headers={"Authorization": f"Bearer {API_KEY}"}
)
print(response.json())