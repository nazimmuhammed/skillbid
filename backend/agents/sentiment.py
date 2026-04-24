from groq import Groq
import os
import random
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class SentimentAgent:
    def __init__(self):
        self.name = "sentiment"
    
    def get_bid(self, task_description: str) -> float:
        if "sentiment" in task_description.lower() or "analyz" in task_description.lower():
            return round(random.uniform(0.001, 0.003), 4)
        return round(random.uniform(0.003, 0.006), 4)
    
    def execute(self, task_description: str) -> str:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a specialized sentiment analysis agent. Provide scores and clear insights."},
                {"role": "user", "content": task_description}
            ]
        )
        return response.choices[0].message.content