import React, { useState, useEffect } from "react";
import { scoreTransaction, getAlerts } from "../api/api";
import RiskCard from "../components/RiskCard";

export default function Dashboard() {
  const [transaction, setTransaction] = useState({
    transaction_id: `TXN_${Date.now()}`,
    customer_id: "CUST_001",
    amount: 12000,
    timestamp: new Date().toISOString(),
    counterparty_country: "KY",
    is_international: true,
  });
  const [alerts, setAlerts] = useState([]);
  const [scoreResult, setScoreResult] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchAlerts();
  }, []);

  const fetchAlerts = async () => {
    try {
      const data = await getAlerts();
      setAlerts(data);
    } catch (err) {
      console.error("Could not fetch alerts", err);
    }
  };

  const handleScore = async () => {
    setLoading(true);
    try {
      const data = await scoreTransaction(transaction);
      setScoreResult(data);
      await fetchAlerts();
    } catch (err) {
      console.error("Scoring error", err);
      alert("Scoring failed. Is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-6">Dashboard</h1>

        <div className="mb-6 bg-white p-4 rounded shadow">
          <h2 className="text-xl font-semibold mb-2">Score Transaction</h2>
          <input
            type="number"
            placeholder="Amount"
            className="border p-2 rounded w-full mb-2"
            value={transaction.amount}
            onChange={(e) => setTransaction({ ...transaction, amount: Number(e.target.value) })}
          />
          <input
            type="text"
            placeholder="Counterparty Country (e.g., KY)"
            className="border p-2 rounded w-full mb-2"
            value={transaction.counterparty_country}
            onChange={(e) => setTransaction({ ...transaction, counterparty_country: e.target.value })}
          />
          <div className="flex items-center gap-3 mt-2">
            <label className="flex items-center gap-2">
              <input
                type="checkbox"
                checked={transaction.is_international}
                onChange={(e) => setTransaction({ ...transaction, is_international: e.target.checked })}
              />
              International
            </label>
            <button onClick={handleScore} disabled={loading} className="bg-blue-600 text-white p-2 rounded">
              {loading ? "Scoring..." : "Score Transaction"}
            </button>
          </div>
        </div>

        {scoreResult && (
          <div className="mb-6">
            <h2 className="text-xl font-semibold mb-2">Result</h2>
            <RiskCard tx={scoreResult} />
          </div>
        )}

        <div>
          <h2 className="text-xl font-semibold mb-2">Top Alerts</h2>
          {alerts.length === 0 && <div>No alerts yet</div>}
          {alerts.map((alert) => (
            <RiskCard key={alert.transaction_id} tx={alert} />
          ))}
        </div>
      </div>
    </div>
  );
}
