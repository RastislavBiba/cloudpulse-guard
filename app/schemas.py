from pydantic import BaseModel, Field
from typing import List, Optional

class AuditRequest(BaseModel):
    code_snippet: str = Field(..., description="Kód infrastruktury (K8s, Dockerfile, Terraform, CEF)")
    code_type: str = Field(default="kubernetes", description="Typ: kubernetes, dockerfile, terraform, cef_log")

class SecurityFinding(BaseModel):
    severity: str = Field(..., description="CRITICAL, HIGH, MEDIUM, LOW, INFO")
    issue: str = Field(..., description="Název a popis zjištěného problému")
    recommendation: str = Field(..., description="Doporučený postup nápravy")

class AuditResult(BaseModel):
    summary: str
    compliance_score: int = Field(..., ge=0, le=100)
    severity: str = "MEDIUM"
    findings: List[SecurityFinding]
    remediated_snippet: Optional[str] = None
    model_used: str
    latency_seconds: float = 0.0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    cost_usd: float = 0.0
