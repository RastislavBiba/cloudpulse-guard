import json
import re
import time
from app.client import get_azure_client
from app.config import AZURE_AI_DEPLOYMENT_NAME
from app.schemas import AuditResult, AuditRequest
from app.guardrails import sanitize_and_check_guardrails
from app.rag import retrieve_relevant_runbook

SYSTEM_PROMPT = """Jsi špičkový Enterprise Cloud Security, SRE & SIEM Incident Auditor (CloudPulse Guard).
Tvým úkolem je provést hloubkovou statickou, bezpečnostní a incidentní prověrku infrastrukturního kódu a logů:
- Kubernetes manifesty, Dockerfile, Terraform
- SIEM / Syslog / CEF (Common Event Format) záznamy, logy API gateway, timeouty Spring WebClient

DŮLEŽITÉ PRO RAG:
Pokud je k požadavku přiložen INTERNÍ SRE RUNBOOK, tvá doporučení a vygenerované nápravné kroky MUSÍ
striktně vycházet z tohoto interního postupu. V souhrnu (summary) přímo uveď název/ID použitého runbooku.

VŠECHNY TEXTY VÝSTUPU MUSÍ BÝT V ČESKÉM JAZYCE.

VŽDY vrať odpověď výhradně jako validní JSON objekt (žádné úvodní ani doplňující texty mimo JSON):
{
  "summary": "Stručný souhrn incidentu s referencí na interní NOTIX runbook v češtině",
  "compliance_score": 30,
  "severity": "CRITICAL",
  "findings": [
    {
      "severity": "CRITICAL",
      "issue": "Název a popis problému v češtině",
      "recommendation": "Doporučený postup nápravy dle interního runbooku v češtině"
    }
  ],
  "remediated_snippet": "Doporučený opravený kód nebo diagnostické CLI příkazy z runbooku"
}
"""

def extract_json(text: str) -> dict:
    """Spolehlivě vytáhne JSON objekt z textu i při výskytu markdown bloků."""
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
                "issue": "Chyba formátování modelu",
                "recommendation": "Zkontrolujte surový výstup v logu.",
            }
        ],
        "remediated_snippet": "# Diagnostika nedostupná",
    }

def run_infrastructure_audit(request: AuditRequest) -> AuditResult:
    start_time = time.time()

    # 1. Kontrola Guardrails (Prompt Injection & Sanitizace PII)
    clean_snippet, guard_status, is_blocked = sanitize_and_check_guardrails(request.code_snippet)
    if is_blocked:
        return AuditResult(
            summary="Audit byl zablokován bezpečnostní politikou Azure AI Guardrails.",
            compliance_score=0,
            severity="CRITICAL",
            findings=[{
                "severity": "CRITICAL",
                "issue": "Prompt Injection / Porušení bezpečnostní politiky",
                "recommendation": "Vstup obsahuje nepovolené instrukce pro manipulaci s chováním modelu."
            }],
            remediated_snippet="# Žádost byla odmítnuta bezpečnostním štítem",
            model_used=f"{AZURE_AI_DEPLOYMENT_NAME} (Guardrails Blokováno)",
            latency_seconds=0.01,
            prompt_tokens=0,
            completion_tokens=0,
            total_tokens=0,
            cost_usd=0.0
        )

    client = get_azure_client()

    # 2. RAG krok: Vyhledání interního SRE Runbooku
    rb_title, rb_content = retrieve_relevant_runbook(clean_snippet)

    # 3. Sestavení obohaceného promptu (Prompt Augmentation)
    user_prompt = (
        f"INTERNÍ FIREMNÍ RUNBOOK ({rb_title}):\n"
        f'"""\n{rb_content}\n"""\n\n'
        f"VSTUP K ANALÝZE ({request.code_type.upper()}):\n"
        f"{clean_snippet}\n\n"
        "Proveď analýzu vstupu striktně dle přiloženého interního runbooku a odpověz v češtině. "
        "Vrať požadovaný JSON objekt."
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
    model_info = f"{AZURE_AI_DEPLOYMENT_NAME} + RAG ({rb_title})"

    return AuditResult(
        summary=parsed_data.get("summary", "Analýza byla úspěšně dokončena."),
        compliance_score=parsed_data.get("compliance_score", 40),
        severity=parsed_data.get("severity", "HIGH"),
        findings=parsed_data.get("findings", []),
        remediated_snippet=parsed_data.get("remediated_snippet", "# Beze změny"),
        model_used=model_info,
        latency_seconds=latency,
        prompt_tokens=in_tokens,
        completion_tokens=out_tokens,
        total_tokens=total_tokens,
        cost_usd=cost_usd,
    )
