import React, { useState } from "react";

function ProofCode({ code }) {
  const [copied, setCopied] = useState(false);

  const fallbackCode = `# No proof code generated for this query`;
  const displayCode = code && code.trim().length > 0 ? code.trim() : fallbackCode;

  const copyCode = () => {
    navigator.clipboard.writeText(displayCode);
    setCopied(true);
    setTimeout(() => {
      setCopied(false);
    }, 2000);
  };

  return (
    <div className="card proof-card">
      <div className="proof-header">
        <div>
          <h3>🧪 Reproducible Proof Code</h3>
          <p>
            Independent Python code executed in an isolated runtime to verify the result.
          </p>
        </div>

        <button
          className="copy-button"
          onClick={copyCode}
        >
          {copied ? "✓ Copied" : "Copy Code"}
        </button>
      </div>

      <pre>
        <code>{displayCode}</code>
      </pre>
    </div>
  );
}

export default ProofCode;