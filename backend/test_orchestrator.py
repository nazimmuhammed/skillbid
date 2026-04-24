from agents.orchestrator import Orchestrator

orchestrator = Orchestrator()

result = orchestrator.run("Summarize this article about climate change in 3 bullet points")

print("\n===== FINAL RESULT =====")
print(f"Winner: {result['winner']}")
print(f"Amount paid: ${result['amount_paid']} USDC")
print(f"Result: {result['result']}")
print("\nAll bids:")
for bid in result['bids']:
    print(f"  {bid['agent_name']}: ${bid['bid_amount']}")