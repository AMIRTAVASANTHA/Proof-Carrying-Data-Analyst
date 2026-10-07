import React, { useState } from "react";
import "./app.css";

import Sidebar from "./components/Sidebar";
import UploadBox from "./components/UploadBox";
import QuestionBox from "./components/QuestionBox";
import ResultCard from "./components/ResultCard";
import ProofCode from "./components/ProofCode";

const EXAMPLE_QUESTIONS = [
  { label: "Category Revenue", query: "Which category has the highest revenue?", type: "standard" },
  { label: "Top Orders State", query: "Which state has the most orders?", type: "standard" },
  { label: "Avg Delivery Time", query: "What is the average delivery time?", type: "standard" },
  { label: "Late Orders (>30d)", query: "How many orders took more than 30 days?", type: "standard" },
  { label: "Monthly Revenue", query: "What is the monthly revenue?", type: "standard" },
  { label: "Profit (Refusal Test)", query: "What is the profit?", type: "refusal" },
  { label: "Salary (Refusal Test)", query: "What is the employee salary?", type: "refusal" },
];

function App() {
  const [question, setQuestion] = useState("");
  const [asked, setAsked] = useState(false);
  const [currentDataset, setCurrentDataset] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [queryHistory, setQueryHistory] = useState([]);

  const handleAsk = async (customQuery) => {
    const queryText = (customQuery || question).trim();
    if (!queryText) {
      alert("Please enter a question.");
      return;
    }

    if (customQuery) {
      setQuestion(customQuery);
    }

    setLoading(true);
    setAsked(false);

    try {
      let response;
      try {
        response = await fetch("/api/ask", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ question: queryText }),
        });
      } catch (err) {
        response = await fetch("http://127.0.0.1:8000/api/ask", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ question: queryText }),
        });
      }

      const data = await response.json();
      setResult(data);
      setAsked(true);
      setQueryHistory((prev) => [
        { text: queryText, verified: data.verified, status: data.status, time: new Date().toLocaleTimeString() },
        ...prev.slice(0, 9),
      ]);
    } catch (error) {
      console.error(error);
      alert("Could not connect to DataProof AI backend. Ensure the server is running on port 8000.");
    } finally {
      setLoading(false);
    }
  };

  const handleUploadSuccess = (data) => {
    setCurrentDataset(data);
  };

  const handleResetDataset = () => {
    setCurrentDataset(null);
  };

  // Determine max value for breakdown chart bars
  const breakdownItems = result?.breakdown || [];
  const maxBarValue = breakdownItems.length > 0
    ? Math.max(...breakdownItems.map((item) => Number(item.value) || 1))
    : 1;

  return (
    <div className="app">
      {/* SIDEBAR */}
      <Sidebar />

      {/* MAIN CONTENT */}
      <main className="main-content">
        {/* TOP BAR */}
        <header className="topbar">
          <div>
            <h1>DataProof AI</h1>
            <p>Proof-Carrying Data Analyst · Mathematical Verification & Anti-Hallucination</p>
          </div>

          <div className="profile">
            <span style={{ fontSize: "12px", background: "#ecfdf5", color: "#047857", padding: "4px 10px", borderRadius: "12px", fontWeight: "bold" }}>
              ● Engine Active
            </span>
            <div className="avatar">A</div>
            <span>Analyst</span>
          </div>
        </header>

        {/* WELCOME SECTION */}
        <section className="welcome">
          <div>
            <span className="ai-badge">🛡️ PROOF-CARRYING DATA ANALYST</span>

            <h2>
              Turn your data into
              <span> mathematically verified answers.</span>
            </h2>

            <p>
              DataProof AI executes trusted baseline tools, synthesizes reproducible Python proof code, runs isolated dual-verification, and refuses to guess when data is missing.
            </p>
          </div>
        </section>

        {/* DATASET UPLOAD */}
        <section className="section">
          <div className="section-title">
            <div>
              <h3>📁 Dataset Scope</h3>
              <p>Active Source: {currentDataset ? `Uploaded File: ${currentDataset.filename}` : "Olist Brazilian E-Commerce Benchmark (100k+ Records)"}</p>
            </div>
          </div>

          <UploadBox
            currentDataset={currentDataset}
            onUploadSuccess={handleUploadSuccess}
            onResetDataset={handleResetDataset}
          />
        </section>

        {/* ASK QUESTION */}
        <section className="section">
          <div className="section-title">
            <div>
              <h3>🤖 Ask Your Data</h3>
              <p>Type any analytical question or select an example below</p>
            </div>
          </div>

          {/* Quick chips */}
          <div style={{ display: "flex", flexWrap: "wrap", gap: "8px", marginBottom: "12px" }}>
            {EXAMPLE_QUESTIONS.map((ex, idx) => (
              <button
                key={idx}
                type="button"
                onClick={() => handleAsk(ex.query)}
                style={{
                  background: ex.type === "refusal" ? "#fef2f2" : "#f5f3ff",
                  color: ex.type === "refusal" ? "#b91c1c" : "#6d28d9",
                  border: `1px solid ${ex.type === "refusal" ? "#fca5a5" : "#ddd6fe"}`,
                  padding: "6px 12px",
                  borderRadius: "16px",
                  fontSize: "12px",
                  cursor: "pointer",
                  fontWeight: 500,
                  transition: "all 0.2s"
                }}
              >
                {ex.type === "refusal" ? "🛡️ " : "⚡ "} {ex.label}
              </button>
            ))}
          </div>

          <QuestionBox
            question={question}
            setQuestion={setQuestion}
            handleAsk={() => handleAsk()}
          />

          {loading && (
            <div className="loading-box" style={{ marginTop: 15, padding: 18, background: "#f8fafc", borderRadius: 10, textAlign: "center", border: "1px dashed #cbd5e1" }}>
              🤖 DataProof AI is analyzing data, generating isolated proof script, and running dual-verification...
            </div>
          )}
        </section>

        {/* RESULTS */}
        {asked && result && (
          <section className="results">
            <ResultCard result={result} />

            {result.status === "success" && (
              <div className="result-grid">
                {/* DYNAMIC CHART */}
                <div className="card chart-card">
                  <div className="card-header">
                    <div>
                      <h3>📊 Analytical Breakdown</h3>
                      <p>Visual verification of top values for this query</p>
                    </div>
                  </div>

                  <div className="chart">
                    {breakdownItems.length > 0 ? (
                      breakdownItems.slice(0, 6).map((item, idx) => {
                        const pct = Math.max(12, Math.min(100, Math.round((Number(item.value) / maxBarValue) * 100)));
                        return (
                          <div className="bar-row" key={idx}>
                            <span title={item.label} style={{ overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                              {item.label}
                            </span>
                            <div className="bar-container">
                              <div className="bar" style={{ width: `${pct}%` }}></div>
                            </div>
                            <b>
                              {typeof item.value === "number" ? item.value.toLocaleString() : item.value}
                            </b>
                          </div>
                        );
                      })
                    ) : (
                      <p style={{ color: "#6b7280", fontSize: "13px", padding: "15px 0" }}>
                        Direct scalar metric calculated: {result.value} {result.unit}
                      </p>
                    )}
                  </div>
                </div>

                {/* DATA SUMMARY */}
                <div className="card summary-card">
                  <h3>📋 Execution Certificate</h3>

                  <div className="summary-item">
                    <span>Rows Analyzed</span>
                    <strong>{result.rows_analyzed ? result.rows_analyzed.toLocaleString() : "96,476+"}</strong>
                  </div>

                  <div className="summary-item">
                    <span>Tables Used</span>
                    <strong>{result.tables_used ? result.tables_used.join(", ") : "Relational"}</strong>
                  </div>

                  <div className="summary-item">
                    <span>Measurement Unit</span>
                    <strong>{result.unit || "Metric"}</strong>
                  </div>

                  <div className="summary-item">
                    <span>Proof Execution</span>
                    <strong className="verified-text">
                      {result.verified ? "✓ Dual-Pass Verified" : "⚠ Refused"}
                    </strong>
                  </div>
                </div>
              </div>
            )}

            {/* PROOF CODE SECTION */}
            {result.generated_code && (
              <ProofCode code={result.generated_code} />
            )}
          </section>
        )}
      </main>
    </div>
  );
}

export default App;