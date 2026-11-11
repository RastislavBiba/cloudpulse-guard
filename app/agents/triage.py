# app/agents/triage.py
import json
import re
from app.config import AZURE_AGENT_TRIAGE_ID
from app.agents_client import execute_agent_run


def run_triage_agent(code_snippet: str, code_type: str) -> tuple[dict, int, int]:
    # FinOps Pruning: Pre klasifikáciu stačí reprezentatívny výrez (max 700 znakov)
    compact_snippet = code_snippet.strip()[:700]
    prompt = f"Typ: {code_type}\nVstup (výrez):\n{compact_snippet}"

    raw_text, p_tok, c_tok = execute_agent_run(AZURE_AGENT_TRIAGE_ID, prompt)

    match = re.search(r"\{.*\}", raw_text, re.DOTALL)
    data = json.loads(match.group(0)) if match else {
        "severity": "HIGH",
        "component": "Neznámá",
        "stack_category": "Infrastruktura",
        "clean_summary": "Zpracování incidentu selhalo."
    }
    return data, p_tok, c_tok
