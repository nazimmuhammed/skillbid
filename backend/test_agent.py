from agents.summarizer import SummarizerAgent

agent = SummarizerAgent()

# Test bidding
bid = agent.get_bid("Please summarize this article about AI")
print(f"Bid amount: ${bid}")

# Test execution
result = agent.execute("Summarize this in 2 sentences: Artificial intelligence is transforming industries worldwide by automating tasks and enabling new capabilities.")
print(f"Result: {result}")