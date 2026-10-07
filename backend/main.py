import os
import sys
import shutil
from pathlib import Path
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import pandas as pd

# -----------------------------------
# Setup paths
# -----------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ANALYSIS_PATH = PROJECT_ROOT / "analysis"
DATA_PATH = PROJECT_ROOT / "data"
UPLOAD_PATH = PROJECT_ROOT / "uploads"
FRONTEND_DIST = PROJECT_ROOT / "frontend" / "dist"

UPLOAD_PATH.mkdir(parents=True, exist_ok=True)

if str(ANALYSIS_PATH) not in sys.path:
    sys.path.append(str(ANALYSIS_PATH))

from query_engine import answer_question
from tool_registry import TOOLS

# -----------------------------------
# FastAPI App
# -----------------------------------
app = FastAPI(
    title="DataProof AI API",
    description="Proof-Carrying Data Analyst AI API",
    version="2.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------------
# Schemas
# -----------------------------------
class QueryRequest(BaseModel):
    question: str
    dataset: Optional[str] = "olist"


class QueryResponse(BaseModel):
    status: str
    question: str
    tool_used: Optional[str] = None
    answer: Optional[str] = None
    value: Optional[Any] = None
    unit: Optional[str] = None
    rows_analyzed: Optional[int] = None
    tables_used: Optional[List[str]] = None
    breakdown: Optional[List[Dict[str, Any]]] = None
    generated_code: Optional[str] = None
    execution_output: Optional[str] = None
    verified: bool = False
    verification_reason: Optional[str] = None
    reason: Optional[str] = None


# -----------------------------------
# API Endpoints
# -----------------------------------
@app.get("/api/health")
def health():
    data_files = [f.name for f in DATA_PATH.glob("*.csv")] if DATA_PATH.exists() else []
    uploaded_files = [f.name for f in UPLOAD_PATH.glob("*")] if UPLOAD_PATH.exists() else []
    return {
        "status": "healthy",
        "version": "2.0",
        "available_datasets": data_files,
        "uploaded_datasets": uploaded_files,
        "supported_tools": list(TOOLS.keys())
    }


@app.get("/api/datasets")
def list_datasets():
    datasets = []
    
    # Olist datasets
    if DATA_PATH.exists():
        for csv_file in DATA_PATH.glob("*.csv"):
            size_mb = round(csv_file.stat().st_size / (1024 * 1024), 2)
            datasets.append({
                "name": csv_file.name,
                "type": "default",
                "size_mb": size_mb,
                "path": str(csv_file.relative_to(PROJECT_ROOT))
            })

    # Uploaded datasets
    if UPLOAD_PATH.exists():
        for up_file in UPLOAD_PATH.glob("*"):
            size_mb = round(up_file.stat().st_size / (1024 * 1024), 2)
            datasets.append({
                "name": up_file.name,
                "type": "uploaded",
                "size_mb": size_mb,
                "path": str(up_file.relative_to(PROJECT_ROOT))
            })

    return {"datasets": datasets}


@app.get("/api/datasets/{dataset_name}/preview")
def preview_dataset(dataset_name: str, rows: int = 5):
    target = None
    if (DATA_PATH / dataset_name).exists():
        target = DATA_PATH / dataset_name
    elif (UPLOAD_PATH / dataset_name).exists():
        target = UPLOAD_PATH / dataset_name
    
    if not target:
        raise HTTPException(status_code=404, detail="Dataset not found")

    try:
        if target.suffix.lower() == ".csv":
            df = pd.read_csv(target, nrows=rows)
        elif target.suffix.lower() in [".xlsx", ".xls"]:
            df = pd.read_excel(target, nrows=rows)
        elif target.suffix.lower() == ".json":
            df = pd.read_json(target).head(rows)
        else:
            raise HTTPException(status_code=400, detail="Unsupported format")

        return {
            "name": dataset_name,
            "columns": list(df.columns),
            "rows_previewed": len(df),
            "sample_data": df.fillna("").to_dict(orient="records")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/upload")
async def upload_dataset(file: UploadFile = File(...)):
    dest_path = UPLOAD_PATH / file.filename
    try:
        with open(dest_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Profile the uploaded dataset
        ext = dest_path.suffix.lower()
        if ext == ".csv":
            df = pd.read_csv(dest_path, nrows=500)
            total_rows = sum(1 for _ in open(dest_path, "r", encoding="utf-8", errors="ignore")) - 1
        elif ext in [".xlsx", ".xls"]:
            df = pd.read_excel(dest_path)
            total_rows = len(df)
        elif ext == ".json":
            df = pd.read_json(dest_path)
            total_rows = len(df)
        else:
            dest_path.unlink()
            raise HTTPException(status_code=400, detail="Only CSV, Excel, or JSON allowed")

        return {
            "status": "success",
            "filename": file.filename,
            "total_rows": max(total_rows, len(df)),
            "columns": list(df.columns),
            "column_types": {col: str(dtype) for col, dtype in df.dtypes.items()},
            "preview": df.head(5).fillna("").to_dict(orient="records")
        }
    except Exception as e:
        if dest_path.exists():
            dest_path.unlink()
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")


@app.post("/ask")
@app.post("/api/ask")
def ask(data: QueryRequest):
    question = data.question.strip()
    if not question:
        return {
            "status": "error",
            "message": "Question is required."
        }

    result = answer_question(question)
    return result


# -----------------------------------
# Static Frontend Serving
# -----------------------------------
if FRONTEND_DIST.exists():
    app.mount("/assets", StaticFiles(directory=str(FRONTEND_DIST / "assets")), name="assets")

    @app.get("/{full_path:path}")
    def serve_frontend(full_path: str):
        file_path = FRONTEND_DIST / full_path
        if file_path.is_file():
            return FileResponse(str(file_path))
        index_file = FRONTEND_DIST / "index.html"
        if index_file.exists():
            return FileResponse(str(index_file))
        return {"message": "DataProof AI backend running"}
else:
    @app.get("/")
    def home():
        return {
            "message": "DataProof AI backend is running. Frontend build not detected yet."
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)