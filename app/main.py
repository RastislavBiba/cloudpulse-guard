from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.schemas import AuditRequest, AuditResult
from app.agents.orchestrator import orchestrate_multi_agent_audit
from app.ui import get_dashboard_html

app = FastAPI(
    title="CloudPulse Guard",
    description="Multi-Agent SRE Incident & Cloud Security Platform napojená na Azure AI Foundry",
    version="2.0.0"
)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "cloudpulse-guard"}

@app.get("/", response_class=HTMLResponse)
def index():
    return get_dashboard_html()

@app.post("/api/audit", response_model=AuditResult)
def audit_endpoint(request: AuditRequest):
    return orchestrate_multi_agent_audit(request)
