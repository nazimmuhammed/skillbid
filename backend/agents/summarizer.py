from groq import Groq
import os
import random

class SummarizerAgent:
    def __init__(self):
        self.name = "summarizer"
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    def get_bid(self, task_description: str) -> float:
        if "summarize" in task_description.lower() or "summary" in task_description.lower():
            return round(random.uniform(0.001, 0.003), 4)
        return round(random.uniform(0.004, 0.007), 4)
    
    def execute(self, task_description: str) -> str:
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a specialized summarization agent. Be concise and clear."},
                {"role": "user", "content": task_description}
            ]
        )
        return response.choices[0].message.content