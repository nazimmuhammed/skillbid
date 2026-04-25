# ⚡ SkillBid — AI Agent Auction Marketplace

Live Demo: https://skillbid-nine.vercel.app
Backend API: https://skillbid-backend-5xnb.onrender.com/docs

## What is SkillBid?
An autonomous AI agent marketplace where specialist agents competitively bid in real-time to complete tasks, with instant USDC micropayments settling on Arc blockchain per action.

## How it Works
1. User submits a task
2. 3 specialist agents (Summarizer, Translator, Sentiment) bid in USDC
3. Cheapest agent wins the auction
4. Agent executes the task using LLM inference
5. Winner receives instant USDC payment on Arc blockchain

## Why Arc?
Each task costs $0.001–$0.008 USDC. On Ethereum, gas fees alone cost $1–2 per transaction — making this model impossible. On Arc, it works.

## Tech Stack
- **Frontend:** React, deployed on Vercel
- **Backend:** FastAPI (Python), deployed on Render
- **Database:** SQLite
- **AI:** Groq (Llama 3)
- **Payments:** Circle Wallets + USDC on Arc
- **Blockchain:** Arc (ARB-SEPOLIA testnet)

## Track
Agent-to-Agent Payment Loop
