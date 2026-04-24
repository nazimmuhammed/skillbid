from payments.circle import get_wallet_balance, send_payment
import time

# Check orchestrator balance first
print("Checking orchestrator balance...")
balance = get_wallet_balance("orchestrator")
print(f"Orchestrator balance: {balance} USDC")

if balance == 0:
    print("No balance yet! Wait for faucet to send USDC and try again.")
else:
    print("\nSending $0.001 USDC from orchestrator to summarizer...")
    result = send_payment("orchestrator", "summarizer", 0.001)
    print(f"\nTransaction result: {result}")