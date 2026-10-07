#!/usr/bin/env python3
"""
DataProof AI - Production Runner
Starts the unified FastAPI backend which serves both the REST API and the bundled React SPA dashboard.
"""
import sys
import os
from pathlib import Path

# Force UTF-8 encoding on standard streams if possible
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.append(str(PROJECT_ROOT / "backend"))
sys.path.append(str(PROJECT_ROOT / "analysis"))

import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "127.0.0.1")

    print("\n" + "=" * 65)
    print(">> DATAPROOF AI - PROOF-CARRYING DATA ANALYST")
    print("=" * 65)
    print(f"Backend & Dashboard URL : http://{host}:{port}")
    print(f"Swagger API Docs        : http://{host}:{port}/docs")
    print(f"API Health Endpoint     : http://{host}:{port}/api/health")
    print("=" * 65 + "\n")

    uvicorn.run("backend.main:app", host=host, port=port, reload=False)
