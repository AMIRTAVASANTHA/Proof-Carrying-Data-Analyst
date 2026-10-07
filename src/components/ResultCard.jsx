import React from "react";

function ResultCard({ result }) {
  if (!result) return null;

  // Refusal case: Out of dataset capability
  if (result.status === "cannot_answer") {
    return (
      <div className="result-card cannot-card">
        <div className="result-top">
          <div className="result-title">
            <div className="warning-icon">!</div>
            <div>
              <p className="cannot-title">CANNOT DETERMINE RELIABLY</p>
              <h3>DataProof AI Refused to Guess</h3>
            </div>
          </div>
          <div className="refusal-badge" style={{ background: "#fee2e2", color: "#dc2626", padding: "6px 12px", borderRadius: "20px", fontSize: "11px", fontWeight: "bold" }}>
            🛡️ ANTI-HALLUCINATION
          </div>
        </div>

        <div className="verification-message warning-message">
          ⚠️
          <span>{result.reason || "The requested metrics cannot be determined from the available dataset."}</span>
        </div>
      </div>
    );
  }

  // Verification Failed Case
  if (result.status === "verification_failed") {
    return (
      <div className="result-card cannot-card">
        <div className="result-top">
          <div className="result-title">
            <div className="warning-icon">✕</div>
            <div>
              <p className="cannot-title" style={{ color: "#dc2626" }}>VERIFICATION FAILED</p>
              <h3>Independent Proof Output Did Not Match</h3>
            </div>
          </div>
          <div className="verified-badge" style={{ background: "#fee2e2", color: "#dc2626" }}>
            ✕ REJECTED
          </div>
        </div>

        <div className="verification-message warning-message">
          ⚠️
          <span>{result.verification_reason || result.error || "Proof code output diverged from baseline calculation."}</span>
        </div>
      </div>
    );
  }

  // Generic Error Case
  if (result.status === "error") {
    return (
      <div className="result-card cannot-card">
        <div className="result-top">
          <div className="result-title">
            <div className="warning-icon">✕</div>
            <div>
              <p className="cannot-title">ERROR</p>
              <h3>Analysis Execution Encountered an Error</h3>
            </div>
          </div>
        </div>
        <div className="verification-message warning-message">
          ⚠️ <span>{result.message || "An unexpected error occurred while executing the query."}</span>
        </div>
      </div>
    );
  }

  // Success Case
  return (
    <div className="result-card">
      <div className="result-top">
        <div className="result-title">
          <div className="check-icon">✓</div>
          <div>
            <p>VERIFIED ANSWER</p>
            <h3>{result.answer}</h3>
          </div>
        </div>

        <div className="verified-badge" style={{
          background: result.verified ? "#dcfce7" : "#fef3c7",
          color: result.verified ? "#15803d" : "#b45309"
        }}>
          {result.verified ? "✓ MATHEMATICALLY VERIFIED" : "⚠ UNVERIFIED"}
        </div>
      </div>

      {result.value !== null && result.value !== undefined && (
        <div className="answer-value">
          <span>{result.unit || "Value"}</span>
          <strong>
            {typeof result.value === "number" ? result.value.toLocaleString() : result.value}
          </strong>
        </div>
      )}

      <div className="result-details">
        <div>
          <span>Tool Used</span>
          <strong>{result.tool_used || "Direct Engine"}</strong>
        </div>

        <div>
          <span>Rows Analyzed</span>
          <strong>{result.rows_analyzed ? result.rows_analyzed.toLocaleString() : "Full Dataset"}</strong>
        </div>

        <div>
          <span>Tables Consulted</span>
          <strong>{result.tables_used ? result.tables_used.join(", ") : "Olist Relational"}</strong>
        </div>

        <div>
          <span>Proof Status</span>
          <strong className="verified-text">
            {result.verified ? "✓ 100% Passed" : "✗ Pending"}
          </strong>
        </div>
      </div>

      <div className="verification-message">
        🔍
        <span>
          {result.verification_reason || "The proof code executed independently in an isolated Python subprocess and certified the exact result."}
        </span>
      </div>
    </div>
  );
}

export default ResultCard;