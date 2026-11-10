# app/main.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from app.schemas import AuditRequest, AuditResult
from app.auditor import run_infrastructure_audit
from app.ui import get_dashboard_html

app = FastAPI(title="CloudPulse Guard", version="1.0.0")

@app.get("/", response_class=HTMLResponse)
def index():
    return get_dashboard_html()

@app.get("/health")
def health():
    return {"status": "ok", "service": "cloudpulse-guard"}

@app.post("/api/audit", response_model=AuditResult)
def audit_code(request: AuditRequest):
    try:
        return run_infrastructure_audit(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
