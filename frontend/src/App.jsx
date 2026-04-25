import { useState, useEffect } from "react"
import axios from "axios"

const API = "https://skillbid-backend-5xnb.onrender.com"
export default function App() {
  const [task, setTask] = useState("")
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [transactions, setTransactions] = useState([])
  const [leaderboard, setLeaderboard] = useState([])
  const [balances, setBalances] = useState({})

  const fetchData = async () => {
    try {
      const [txRes, lbRes, balRes] = await Promise.all([
        axios.get(`${API}/api/transactions`),
        axios.get(`${API}/api/leaderboard`),
        axios.get(`${API}/api/balances`)
      ])
      setTransactions(txRes.data)
      setLeaderboard(lbRes.data)
      setBalances(balRes.data)
    } catch (e) { console.error(e) }
  }

  useEffect(() => {
    fetchData()
    const interval = setInterval(fetchData, 5000)
    return () => clearInterval(interval)
  }, [])

  const submitTask = async () => {
    if (!task.trim()) return
    setLoading(true)
    setResult(null)
    try {
      const res = await axios.post(`${API}/api/task`, { description: task, max_budget: 0.01 })
      setResult(res.data)
      fetchData()
    } catch (e) { console.error(e) }
    setLoading(false)
  }

  return (
    <div style={{ minHeight: "100vh", background: "linear-gradient(135deg, #0a0a1a 0%, #0d1b2a 50%, #0a0a1a 100%)", color: "#fff", padding: "24px", fontFamily: "'Inter', system-ui, sans-serif" }}>
      
      {/* Animated background dots */}
      <div style={{ position: "fixed", inset: 0, backgroundImage: "radial-gradient(circle, #ffffff08 1px, transparent 1px)", backgroundSize: "40px 40px", pointerEvents: "none" }} />
      
      <div style={{ maxWidth: "1100px", margin: "0 auto", position: "relative" }}>
        
        {/* Header */}
        <div style={{ textAlign: "center", marginBottom: "40px" }}>
          <div style={{ display: "inline-block", background: "linear-gradient(135deg, #3b82f6, #8b5cf6)", borderRadius: "16px", padding: "2px", marginBottom: "16px" }}>
            <div style={{ background: "#0a0a1a", borderRadius: "14px", padding: "8px 24px" }}>
              <span style={{ fontSize: "13px", color: "#a78bfa", fontWeight: "600", letterSpacing: "2px" }}>POWERED BY ARC + CIRCLE USDC</span>
            </div>
          </div>
          <h1 style={{ fontSize: "56px", fontWeight: "800", background: "linear-gradient(135deg, #fff 0%, #a78bfa 50%, #3b82f6 100%)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent", marginBottom: "12px" }}>⚡ SkillBid</h1>
          <p style={{ color: "#6b7280", fontSize: "18px" }}>AI Agents compete. Cheapest wins. USDC settles on Arc.</p>
        </div>

        {/* Balances */}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: "16px", marginBottom: "32px" }}>
          {Object.entries(balances).length === 0 ? ["orchestrator","summarizer","translator","sentiment"].map(a => (
            <div key={a} style={{ background: "linear-gradient(135deg, #111827, #1f2937)", borderRadius: "16px", padding: "20px", border: "1px solid #ffffff15", backdropFilter: "blur(10px)" }}>
              <p style={{ color: "#6b7280", fontSize: "12px", textTransform: "uppercase", letterSpacing: "1px", marginBottom: "8px" }}>{a}</p>
              <p style={{ color: "#34d399", fontSize: "24px", fontWeight: "700" }}>$0.00</p>
              <p style={{ color: "#4b5563", fontSize: "11px" }}>USDC on Arc</p>
            </div>
          )) : Object.entries(balances).map(([agent, balance]) => (
            <div key={agent} style={{ background: "linear-gradient(135deg, #111827, #1f2937)", borderRadius: "16px", padding: "20px", border: "1px solid #ffffff15", backdropFilter: "blur(10px)" }}>
              <p style={{ color: "#6b7280", fontSize: "12px", textTransform: "uppercase", letterSpacing: "1px", marginBottom: "8px" }}>{agent}</p>
              <p style={{ color: "#34d399", fontSize: "24px", fontWeight: "700" }}>${Number(balance).toFixed(4)}</p>
              <p style={{ color: "#4b5563", fontSize: "11px" }}>USDC on Arc</p>
            </div>
          ))}
        </div>

        {/* Task Input */}
        <div style={{ background: "linear-gradient(135deg, #111827, #1a1f35)", borderRadius: "20px", padding: "28px", border: "1px solid #ffffff15", marginBottom: "24px", boxShadow: "0 0 40px #3b82f620" }}>
          <h2 style={{ fontSize: "20px", fontWeight: "700", marginBottom: "16px", color: "#e5e7eb" }}>🎯 Submit a Task</h2>
          <textarea
            style={{ width: "100%", background: "#0d1117", borderRadius: "12px", padding: "16px", color: "#fff", border: "1px solid #ffffff20", fontSize: "15px", resize: "none", height: "100px", outline: "none", boxSizing: "border-box", lineHeight: "1.6" }}
            placeholder="e.g. Summarize the impact of AI on healthcare in 3 bullet points..."
            value={task}
            onChange={e => setTask(e.target.value)}
          />
          <button
            onClick={submitTask}
            disabled={loading}
            style={{ marginTop: "16px", background: loading ? "#1f2937" : "linear-gradient(135deg, #3b82f6, #8b5cf6)", color: loading ? "#6b7280" : "#fff", fontWeight: "700", padding: "14px 36px", borderRadius: "12px", border: "none", cursor: loading ? "not-allowed" : "pointer", fontSize: "15px", transition: "all 0.2s", boxShadow: loading ? "none" : "0 0 20px #3b82f640" }}
          >
            {loading ? "⏳ Agents are bidding..." : "🚀 Submit Task"}
          </button>
        </div>

        {/* Result */}
        {result && (
          <div style={{ background: "linear-gradient(135deg, #052e16, #111827)", borderRadius: "20px", padding: "28px", border: "1px solid #16a34a40", marginBottom: "24px", boxShadow: "0 0 40px #16a34a20" }}>
            <h2 style={{ fontSize: "20px", fontWeight: "700", marginBottom: "20px", color: "#4ade80" }}>✅ Auction Complete</h2>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "12px", marginBottom: "20px" }}>
              {result.bids.map(bid => (
                <div key={bid.agent_name} style={{ borderRadius: "12px", padding: "16px", border: bid.agent_name === result.winner ? "1px solid #22c55e" : "1px solid #ffffff15", background: bid.agent_name === result.winner ? "#14532d40" : "#ffffff08", transition: "all 0.2s" }}>
                  <p style={{ fontWeight: "700", textTransform: "capitalize", marginBottom: "6px", fontSize: "15px" }}>{bid.agent_name} {bid.agent_name === result.winner ? "🏆" : ""}</p>
                  <p style={{ color: "#fbbf24", fontSize: "20px", fontWeight: "700" }}>${bid.bid_amount}</p>
                  <p style={{ color: "#6b7280", fontSize: "12px" }}>USDC bid</p>
                </div>
              ))}
            </div>
            <div style={{ background: "#0d1117", borderRadius: "12px", padding: "16px", marginBottom: "12px" }}>
              <p style={{ color: "#9ca3af", fontSize: "13px", marginBottom: "4px" }}>Winner: <span style={{ color: "#4ade80", fontWeight: "700", textTransform: "capitalize" }}>{result.winner}</span> — Paid <span style={{ color: "#fbbf24", fontWeight: "700" }}>${result.amount_paid} USDC</span></p>
              <p style={{ color: "#4b5563", fontSize: "11px", wordBreak: "break-all" }}>TX Hash: {result.tx_hash}</p>
            </div>
            <div style={{ background: "#0d1117", borderRadius: "12px", padding: "16px" }}>
              <p style={{ color: "#6b7280", fontSize: "13px", marginBottom: "8px" }}>Task Result:</p>
              <p style={{ color: "#e5e7eb", whiteSpace: "pre-wrap", lineHeight: "1.7", fontSize: "14px" }}>{result.result}</p>
            </div>
          </div>
        )}

        {/* Bottom Grid */}
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "24px" }}>
          <div style={{ background: "linear-gradient(135deg, #111827, #1a1f35)", borderRadius: "20px", padding: "24px", border: "1px solid #ffffff15" }}>
            <h2 style={{ fontSize: "18px", fontWeight: "700", marginBottom: "20px" }}>🏆 Agent Leaderboard</h2>
            {leaderboard.length === 0 ? <p style={{ color: "#4b5563" }}>Submit a task to start the auction!</p> :
              leaderboard.map((a, i) => (
                <div key={a.agent} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "12px 0", borderBottom: "1px solid #ffffff10" }}>
                  <span style={{ textTransform: "capitalize", fontSize: "15px" }}>{i === 0 ? "🥇" : i === 1 ? "🥈" : "🥉"} {a.agent}</span>
                  <div style={{ textAlign: "right" }}>
                    <p style={{ color: "#34d399", fontWeight: "700" }}>${Number(a.total_earned).toFixed(4)}</p>
                    <p style={{ color: "#6b7280", fontSize: "12px" }}>{a.tasks_completed} tasks</p>
                  </div>
                </div>
              ))
            }
          </div>

          <div style={{ background: "linear-gradient(135deg, #111827, #1a1f35)", borderRadius: "20px", padding: "24px", border: "1px solid #ffffff15" }}>
            <h2 style={{ fontSize: "18px", fontWeight: "700", marginBottom: "20px" }}>⛓️ Live Transactions</h2>
            {transactions.length === 0 ? <p style={{ color: "#4b5563" }}>No transactions yet</p> :
              transactions.slice(0, 6).map(tx => (
                <div key={tx.id} style={{ padding: "12px 0", borderBottom: "1px solid #ffffff10" }}>
                  <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "4px" }}>
                    <span style={{ color: "#fbbf24", fontWeight: "700" }}>${Number(tx.amount).toFixed(4)} USDC</span>
                    <span style={{ color: "#34d399", fontSize: "12px", background: "#052e1640", padding: "2px 8px", borderRadius: "6px" }}>{tx.status}</span>
                  </div>
                  <p style={{ color: "#4b5563", fontSize: "11px", wordBreak: "break-all" }}>{tx.tx_hash?.slice(0, 40)}...</p>
                </div>
              ))
            }
          </div>
        </div>

      </div>
    </div>
  )
}