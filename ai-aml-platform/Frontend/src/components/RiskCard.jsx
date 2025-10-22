import React from "react";

export default function RiskCard({ tx }) {
  const label = tx.label || (tx.risk_score >= 0.8 ? "Suspicious" : tx.risk_score >= 0.6 ? "Medium" : "Normal");
  let bgColor = "bg-green-100";
  if (label === "Medium") bgColor = "bg-yellow-100";
  if (label === "Suspicious") bgColor = "bg-red-100";

  const reasons = tx.reasons || [];

  return (
    <div className={`p-4 rounded shadow ${bgColor} mb-3`}>
      <div><strong>ID:</strong> {tx.transaction_id}</div>
      <div><strong>Amount:</strong> {tx.amount}</div>
      <div><strong>Risk Score:</strong> {(tx.risk_score || 0).toFixed(2)} ({label})</div>
      <div><strong>Reasons:</strong> {reasons.length ? reasons.join(", ") : "—"}</div>
    </div>
  );
}
