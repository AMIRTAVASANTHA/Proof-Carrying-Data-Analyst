# DataProof AI 🛡️📊

> **Proof-Carrying Data Analyst AI**  
> Mathematically verified, anti-hallucination data intelligence with isolated dual-execution proofs.

---

## Overview

Traditional AI data assistants frequently fabricate metrics, produce answers without reproducible derivations, or hallucinate when data columns are missing.

**DataProof AI** guarantees mathematical reliability using a **Proof-Carrying Analysis Pipeline**:
1. **Capability Gate (Anti-Hallucination)**: Strictly analyzes whether the dataset has the required fields before computing. If fields are missing (e.g. asking for "profit" when only product prices are provided), it refuses to guess and explains why.
2. **Trusted Analytical Baseline**: Computes trusted ground truth metrics using verified analytical libraries.
3. **Reproducible Proof Code Synthesis**: Synthesizes standalone, self-contained Python scripts for the exact calculation.
4. **Subprocess Isolation**: Executes the generated proof script in an isolated runtime environment.
5. **Dual-Pass Mathematical Certification**: Compares the baseline output with the proof output and issues a cryptographic/formal proof certificate.

---

## Architecture

```
DataProof-AI/
├── backend/
│   └── main.py             # FastAPI server (API routes, upload, static SPA serving)
├── analysis/
│   ├── capability_checker.py # Anti-hallucination capability gate
│   ├── question_parser.py    # Query intent recognition
│   ├── analytics_tools.py    # Trusted analytical tools
│   ├── tool_registry.py      # Available analysis tools
│   ├── code_generator.py     # Python proof code synthesis
│   ├── code_executor.py      # Subprocess execution sandbox
│   ├── result_verifier.py    # Dual-pass verification engine
│   ├── query_engine.py       # Orchestrated proof pipeline
│   └── data_loader.py        # Dynamic relational data loader
├── agent/
│   ├── agent.py              # LLM / Heuristic proof-carrying agent
│   └── llm.py                # LLM decision interface with fallback
├── data/                     # Olist Brazilian E-Commerce Benchmark
├── frontend/                 # Modern React + Vite Dashboard
│   ├── dist/                 # Pre-built production SPA
│   └── src/                  # React source components
├── tests/
│   └── test_dataproof.py     # End-to-end integration test suite
├── requirements.txt          # Python dependencies
├── run_app.py                # Unified launcher
└── start.bat                 # 1-click Windows launcher
```

---

## Quickstart

### 1. Requirements
- Python 3.10+
- Node.js 20+ (Optional, only needed if modifying React components; pre-built bundle is included in `frontend/dist`)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the Application
```bash
python run_app.py
```
Or double-click `start.bat` on Windows.

Open your browser to:
- **Interactive Dashboard**: `http://localhost:8000`
- **Swagger API Documentation**: `http://localhost:8000/docs`
- **Health Check**: `http://localhost:8000/api/health`

---

## Example Queries to Try

| Question | Expected Behavior | Verification Status |
| :--- | :--- | :--- |
| **"Which category has the highest revenue?"** | Identifies `health_beauty` with R$ 1,258,681.34 | ✓ **VERIFIED** |
| **"Which state has the most orders?"** | Identifies `SP` with 41,746 orders | ✓ **VERIFIED** |
| **"What is the average delivery time?"** | Computes 12.56 days across 96,476 orders | ✓ **VERIFIED** |
| **"How many orders took more than 30 days?"** | Computes 4,553 delayed orders | ✓ **VERIFIED** |
| **"What is the profit?"** | **Refusal**: Explains cost/expense data is missing | 🛡️ **ANTI-HALLUCINATION** |
| **"What is the employee salary?"** | **Refusal**: Explains HR data is missing | 🛡️ **ANTI-HALLUCINATION** |

---

## Running Automated Tests

Run the full end-to-end verification test suite:

```bash
pytest tests/test_dataproof.py -v
```

All 6 test suites verify:
- Relational dataset loading across 100,000+ records
- Anti-hallucination refusal for out-of-scope queries
- Mathematical consistency between analytical tools and generated proof scripts
- Subprocess isolation and execution stability
- FastAPI REST endpoints
