import React, { useState } from "react";

function UploadBox({ onUploadSuccess, currentDataset, onResetDataset }) {
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState(null);

  const handleFile = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setUploading(true);
    setUploadError(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("/api/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        // Try fallback to absolute URL if relative fails
        const fallbackRes = await fetch("http://127.0.0.1:8000/api/upload", {
          method: "POST",
          body: formData,
        });
        if (!fallbackRes.ok) {
          throw new Error("Upload failed. Server responded with " + fallbackRes.status);
        }
        const data = await fallbackRes.json();
        if (onUploadSuccess) onUploadSuccess(data);
        return;
      }

      const data = await response.json();
      if (onUploadSuccess) onUploadSuccess(data);
    } catch (err) {
      console.error("Upload error:", err);
      setUploadError(err.message || "Failed to upload dataset.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="upload-box">
      {!currentDataset ? (
        <>
          <div className="upload-icon">📤</div>
          <h3>Upload Your Custom Dataset</h3>
          <p>Analyze CSV, Excel or JSON with verified mathematical proofs</p>

          <label className="upload-button">
            {uploading ? "Analyzing Dataset..." : "Choose File"}
            <input
              type="file"
              accept=".csv,.xlsx,.xls,.json"
              onChange={handleFile}
              disabled={uploading}
            />
          </label>

          <small>Supported formats: CSV, Excel, JSON (e.g., sales, orders, finance)</small>
          {uploadError && <p className="error-text" style={{ color: "#dc2626", marginTop: 8, fontSize: 12 }}>{uploadError}</p>}
        </>
      ) : (
        <div className="uploaded-file">
          <div className="file-icon">📊</div>
          <div className="file-info">
            <h3>{currentDataset.filename || currentDataset.name}</h3>
            <p>
              ✓ Ready for analysis · {currentDataset.total_rows?.toLocaleString() || "Dataset loaded"} rows · {currentDataset.columns?.length || 0} columns
            </p>
            {currentDataset.columns && (
              <div style={{ fontSize: "11px", color: "#6b7280", marginTop: "4px" }}>
                Columns: {currentDataset.columns.slice(0, 6).join(", ")}{currentDataset.columns.length > 6 ? "..." : ""}
              </div>
            )}
          </div>
          <button className="remove-button" onClick={onResetDataset}>
            Reset to Default
          </button>
        </div>
      )}
    </div>
  );
}

export default UploadBox;