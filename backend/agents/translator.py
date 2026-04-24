from groq import Groq
import os
import random
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class TranslatorAgent:
    def __init__(self):
        self.name = "translator"
    
    def get_bid(self, task_description: str) -> float:
        if "translat" in task_description.lower():
            return round(random.uniform(0.001, 0.003), 4)
        return round(random.uniform(0.004, 0.008), 4)
    
    def execute(self, task_description: str) -> str:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a specialized translation agent. Be accurate and natural."},
                {"role": "user", "content": task_description}
            ]
        )
        return response.choices[0].message.content