# app/agents/remediation.py
import json
import re
from app.config import AZURE_AGENT_REMEDIATION_ID
from app.agents_client import execute_agent_run


def run_remediation_agent(triage_data: dict, code_snippet: str, runbook_title: str, runbook_content: str) -> tuple[
    dict, int, int]:
    # FinOps Pruning: Odovzdáme len podstatnú časť vstupu bez nadbytočných bielych znakov
    compact_snippet = code_snippet.strip()[:1200]

    prompt = f"""RUNBOOK ({runbook_title}):
\"\"\"
{runbook_content.strip()}
\"\"\"

KONTEXT:
Komponenta: {triage_data.get('component')} | Závažnost: {triage_data.get('severity')}
Problém: {triage_data.get('clean_summary')}

VSTUP:
{compact_snippet}
"""
    raw_text, p_tok, c_tok = execute_agent_run(AZURE_AGENT_REMEDIATION_ID, prompt)

    match = re.search(r"\{.*\}", raw_text, re.DOTALL)
    data = json.loads(match.group(0)) if match else {
        "findings": [{"severity": triage_data.get("severity", "HIGH"), "issue": "Chyba generování nápravy",
                      "recommendation": "Zkontrolujte systémové logy."}],
        "remediated_snippet": "# Nápravný krok se nepodařilo vygenerovat"
    }
    return data, p_tok, c_tok
