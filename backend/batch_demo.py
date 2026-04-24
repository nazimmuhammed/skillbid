import httpx
import time

API = "http://localhost:8000"

tasks = [
    "Summarize the impact of AI on healthcare in 3 bullet points",
    "Translate 'Hello, how are you?' to French",
    "Analyze sentiment: This product is terrible, worst purchase ever",
    "Summarize the history of the internet in 2 sentences",
    "Translate 'Good morning' to Spanish, French, and German",
    "Analyze sentiment: I love this restaurant, food was incredible",
    "Summarize quantum computing in simple terms",
    "Translate 'Thank you very much' to Japanese",
    "Analyze sentiment: The movie was okay, nothing special",
    "Summarize the benefits of renewable energy",
    "Translate 'Where is the nearest hospital?' to Arabic",
    "Analyze sentiment: Best customer service I have ever experienced!",
    "Summarize the causes of World War 1",
    "Translate 'I need help' to Mandarin",
    "Analyze sentiment: The delivery was late and packaging was damaged",
    "Summarize the main benefits of exercise",
    "Translate 'Happy Birthday' to Italian",
    "Analyze sentiment: This laptop is fast and reliable, very happy",
    "Summarize how blockchain technology works",
    "Translate 'Please call me tomorrow' to Portuguese",
]

print(f"Running {len(tasks)} tasks...")
print("This will generate 20+ transactions on Arc\n")

success = 0
failed = 0

for i, task in enumerate(tasks):
    try:
        res = httpx.post(
            f"{API}/api/task",
            json={"description": task, "max_budget": 0.01},
            timeout=30
        )
        data = res.json()
        print(f"[{i+1}/{len(tasks)}] ✅ Winner: {data['winner']} | Paid: ${data['amount_paid']} | TX: {data['tx_hash'][:20]}...")
        success += 1
        time.sleep(1)
    except Exception as e:
        print(f"[{i+1}/{len(tasks)}] ❌ Failed: {e}")
        failed += 1

print(f"\n===== BATCH COMPLETE =====")
print(f"✅ Successful: {success}")
print(f"❌ Failed: {failed}")
print(f"Total transactions generated: {success}")
print(f"\nCheck your dashboard at http://localhost:5173")