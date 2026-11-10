# app/auditor.py
import json
import re
import time
from app.client import get_azure_client
from app.config import AZURE_AI_DEPLOYMENT_NAME
from app.schemas import AuditResult, AuditRequest

SYSTEM_PROMPT = """Si špičkový Enterprise Cloud Security, SRE & SIEM Incident Auditor (CloudPulse Guard).
Tvojou úlohou je vykonať hĺbkovú statickú, bezpečnostnú a incidentnú previerku infraštruktúrneho kódu a logov:
- Kubernetes manifesty, Dockerfile, Terraform
- SIEM / Syslog / CEF (Common Event Format) záznamy, API gateway logy, Spring WebClient timeouty

Ak analyzuješ CEF / Syslog záznam:
1. Zanalyzuj polia (cs1=ApplicationName, cs5=RequestUrl, cs6=Msg, severity, cieľovú IP a DNS).
2. Urči kořenovú príčinu (napr. DNS resolution, Firewall / Egress security group, výpadok IdP/autority).
3. V "findings" popíš dopad na dostupnosť a bezpečnosť.
4. V "remediated_snippet" navrhni SRE runbook / sieťové príkazy na overenie (curl, dig, traceroute, nastavenie circuit breakera / timeoutu vo WebClientovi).

VŽDY vráť odpoveď výhradne ako validný JSON objekt (žiadne úvodné ani sprievodné texty):
{
  "summary": "Stručné zhrnutie incidentu pre ticket",
  "compliance_score": 30,
  "severity": "CRITICAL",
  "findings": [
    {
      "severity": "CRITICAL",
      "issue": "Názov a popis problému",
      "recommendation": "Odporúčaný postup nápravy"
    }
  ],
  "remediated_snippet": "Odporúčaný opravený kód alebo diagnostické CLI príkazy"
}
"""


def extract_json(text: str) -> dict:
    """Spoľahlivo vytiahne JSON objekt z textu aj pri markdown blokoch."""
    text = text.strip()
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass
    return {
        "summary": text[:200] + "...",
        "compliance_score": 50,
        "severity": "HIGH",
        "findings": [
            {
                "severity": "HIGH",
                "issue": "Chyba formátovania modelu",
                "recommendation": "Skontrolujte surový výstup v logoch.",
            }
        ],
        "remediated_snippet": "# Diagnostika nedostupná",
    }


def run_infrastructure_audit(request: AuditRequest) -> AuditResult:
    start_time = time.time()
    client = get_azure_client()

    user_prompt = (
        f"Vykonaj audit / incidentnú analýzu tohto vstupu ({request.code_type.upper()}):\n\n"
        f"{request.code_snippet}\n\n"
        "Vráť požadovaný JSON objekt s analýzou a nápravnými krokmi."
    )

    response = client.chat.completions.create(
        model=AZURE_AI_DEPLOYMENT_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )

    latency = round(time.time() - start_time, 2)
    raw_content = response.choices[0].message.content or ""
    parsed_data = extract_json(raw_content)

    in_tokens = 0
    out_tokens = 0
    total_tokens = 0
    if hasattr(response, "usage") and response.usage:
        in_tokens = response.usage.prompt_tokens or 0
        out_tokens = response.usage.completion_tokens or 0
        total_tokens = response.usage.total_tokens or 0

    cost_usd = round((in_tokens * 0.00000015) + (out_tokens * 0.00000060), 6)

    return AuditResult(
        summary=parsed_data.get("summary", "Analýza dokončená."),
        compliance_score=parsed_data.get("compliance_score", 40),
        severity=parsed_data.get("severity", "HIGH"),
        findings=parsed_data.get("findings", []),
        remediated_snippet=parsed_data.get("remediated_snippet", "# Bez zmeny"),
        model_used=AZURE_AI_DEPLOYMENT_NAME,
        latency_seconds=latency,
        prompt_tokens=in_tokens,
        completion_tokens=out_tokens,
        total_tokens=total_tokens,
        cost_usd=cost_usd,
    )
