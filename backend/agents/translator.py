from groq import Groq
import os
import random

class TranslatorAgent:
    def __init__(self):
        self.name = "translator"
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    def get_bid(self, task_description: str) -> float:
        if "translate" in task_description.lower():
            return round(random.uniform(0.001, 0.003), 4)
        return round(random.uniform(0.004, 0.007), 4)
    
    def execute(self, task_description: str) -> str:
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a specialized translation agent. Translate accurately."},
                {"role": "user", "content": task_description}
            ]
        )
        return response.choices[0].message.content