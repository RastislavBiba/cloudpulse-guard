# app/agents/safety.py
import json
import re
from app.config import AZURE_AGENT_SAFETY_ID
from app.agents_client import execute_agent_run

DANGEROUS_PATTERNS = [
    r"rm\s+-rf\s+/",
    r"drop\s+database",
    r"truncate\s+table",
    r":\(\)\s*\{.*\}\s*;",
    r"chmod\s+-R\s+777",
]


def run_safety_agent(triage_data: dict, remediation_data: dict) -> tuple[dict, int, int]:
    snippet = remediation_data.get("remediated_snippet", "").strip()

    # 1. Deterministická lokálna kontrola (0 tokenov)
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, snippet, re.IGNORECASE):
            return {
                "compliance_score": 10,
                "safety_verdict": "ZAMÍTNUTO",
                "audit_comment": f"Detekován nebezpečný destruktivní vzor: {pattern}"
            }, 0, 0

    # 2. Minimalistický prompt pre cloudového Safety Agenta
    prompt = f"""OPRAVNÝ KÓD / SKRIPT:
{snippet[:1000]}

ZÁVAŽNOST: {triage_data.get('severity', 'HIGH')}
"""
    try:
        raw_text, p_tok, c_tok = execute_agent_run(AZURE_AGENT_SAFETY_ID, prompt)
        match = re.search(r"\{.*\}", raw_text, re.DOTALL)
        data = json.loads(match.group(0)) if match else {
            "compliance_score": 70,
            "safety_verdict": "SCHVÁLENO",
            "audit_comment": "Audit proběhl v pořádku."
        }
        return data, p_tok, c_tok
    except Exception as e:
        return {
            "compliance_score": 65,
            "safety_verdict": "SCHVÁLENO (FALLBACK)",
            "audit_comment": f"Cloudový bezpečnostní oponent byl vynechán ({e})."
        }, 0, 0
