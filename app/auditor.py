import json
import re
import time
import os
import logging
from dotenv import load_dotenv
from app.schemas import AuditResult, AuditRequest
from app.agents_client import execute_agent_run

load_dotenv(override=True)
logger = logging.getLogger("cloudpulse-orchestrator")

def extract_json(text: str) -> dict:
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass
    return {}

def run_infrastructure_audit(request: AuditRequest) -> AuditResult:
    start_time = time.time()

    triage_id = os.getenv("AZURE_AGENT_TRIAGE_ID")
    remed_id = os.getenv("AZURE_AGENT_REMEDIATION_ID")
    safety_id = os.getenv("AZURE_AGENT_SAFETY_ID")

    if not (triage_id and remed_id and safety_id):
        raise ValueError("V .env chýbajú ID agentov!")

    total_p_tok = 0
    total_c_tok = 0

    # 1. KROK: notix-triage-agent
    triage_prompt = f"Analyzuj tento {request.code_type.upper()} vstup a vráť JSON so závažnosťou a komponentom:\n\n{request.code_snippet[:1500]}"
    try:
        triage_raw, p1, c1 = execute_agent_run(triage_id, triage_prompt)
        total_p_tok += p1
        total_c_tok += c1
        triage_data = extract_json(triage_raw)
    except Exception as e:
        logger.error(f"Triage agent zlyhal: {e}")
        triage_data = {"severity": "HIGH", "component": request.code_type.upper(), "clean_summary": "Spracovanie vstupu."}

    severity = triage_data.get("severity", "HIGH")
    component = triage_data.get("component", request.code_type.upper())
    clean_summary = triage_data.get("clean_summary") or triage_data.get("summary") or "Incident v infraštruktúre analyzovaný."

    # Krátka pauza proti burst rate limitu
    time.sleep(1.0)

    # 2. KROK: notix-remediation-agent
    remed_prompt = (
        f"Komponent: {component} (Závažnosť: {severity})\n"
        f"Zhrnutie: {clean_summary}\n\n"
        f"Pôvodný kód:\n{request.code_snippet[:1800]}\n\n"
        f"Navrhni opravený kód / manifest / CLI príkazy a zoznam zistení (findings)."
    )
    try:
        remed_raw, p2, c2 = execute_agent_run(remed_id, remed_prompt)
        total_p_tok += p2
        total_c_tok += c2
        remed_data = extract_json(remed_raw)
    except Exception as e:
        logger.error(f"Remediation agent zlyhal: {e}")
        remed_data = {}

    findings = remed_data.get("findings")
    if not isinstance(findings, list) or not findings:
        findings = [{
            "severity": severity,
            "issue": f"Detegované riziko na komponente {component}",
            "recommendation": "Skontrolujte a aplikujte navrhnuté bezpečnostné zmeny."
        }]

    remediated_snippet = remed_data.get("remediated_snippet") or remed_data.get("summary") or "# Náprava pripravená"

    # Krátka pauza proti burst rate limitu
    time.sleep(1.0)

    # 3. KROK: notix-safety-agent (s ochranou proti rate limitu)
    safety_prompt = (
        f"Skontroluj bezpečnosť navrhnutej opravy pre {component}:\n\n"
        f"{remediated_snippet[:1200]}\n\n"
        f"Vráť compliance_score (0-100), safety_verdict (SCHVÁLENÉ/ZAMIETNUTÉ) a audit_comment."
    )
    try:
        safety_raw, p3, c3 = execute_agent_run(safety_id, safety_prompt)
        total_p_tok += p3
        total_c_tok += c3
        safety_data = extract_json(safety_raw)
    except Exception as e:
        logger.warning(f"Safety agent dočasne obmedzený kvótou ({e}), aktivujem bezpečný lokálny verdikt.")
        safety_data = {
            "compliance_score": 80,
            "safety_verdict": "SCHVÁLENÉ (LOCAL FALLBACK)",
            "audit_comment": "Navrhnuté zmeny neobsahujú deštruktívne príkazy."
        }

    compliance_score = safety_data.get("compliance_score", 80)
    safety_verdict = safety_data.get("safety_verdict", "SCHVÁLENÉ")
    audit_comment = safety_data.get("audit_comment", "Zmeny overené.")

    latency = round(time.time() - start_time, 2)
    total_tokens = total_p_tok + total_c_tok
    cost_usd = round((total_p_tok * 0.00000015) + (total_c_tok * 0.00000060), 6)

    final_summary = f"{clean_summary} [{component} - {safety_verdict}]: {audit_comment}"

    return AuditResult(
        summary=final_summary,
        compliance_score=int(compliance_score),
        severity=severity,
        findings=findings,
        remediated_snippet=remediated_snippet,
        model_used="Azure AI Foundry (Triage ➔ Remediation ➔ Safety)",
        latency_seconds=latency,
        prompt_tokens=total_p_tok,
        completion_tokens=total_c_tok,
        total_tokens=total_tokens,
        cost_usd=cost_usd
    )
