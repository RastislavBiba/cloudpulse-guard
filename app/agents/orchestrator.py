# app/agents/orchestrator.py
import time
from app.config import AZURE_AI_DEPLOYMENT_NAME
from app.schemas import AuditResult, AuditRequest
from app.guardrails import sanitize_and_check_guardrails
from app.rag import retrieve_relevant_runbook
from app.agents.triage import run_triage_agent
from app.agents.remediation import run_remediation_agent
from app.agents.safety import run_safety_agent


def orchestrate_multi_agent_audit(request: AuditRequest) -> AuditResult:
    start_time = time.time()

    # 1. Guardrails kontrola vstupu
    clean_snippet, guard_status, is_blocked = sanitize_and_check_guardrails(request.code_snippet)
    if is_blocked:
        return AuditResult(
            summary="Audit byl zablokován bezpečnostní politikou Azure AI Guardrails.",
            compliance_score=0,
            severity="CRITICAL",
            findings=[{
                "severity": "CRITICAL",
                "issue": "Prompt Injection / Porušení bezpečnostní politiky",
                "recommendation": "Vstup obsahuje nepovolené instrukce."
            }],
            remediated_snippet="# Žádost byla odmítnuta bezpečnostním štítem",
            model_used=f"{AZURE_AI_DEPLOYMENT_NAME} (Guardrails Blokováno)",
            latency_seconds=0.01,
            prompt_tokens=0,
            completion_tokens=0,
            total_tokens=0,
            cost_usd=0.0
        )

    total_prompt_tokens = 0
    total_completion_tokens = 0

    # 2. Sub-Agent 1: Triage
    triage_data, p_tok1, c_tok1 = run_triage_agent(clean_snippet, request.code_type)
    total_prompt_tokens += p_tok1
    total_completion_tokens += c_tok1

    # Malá pauza proti 429 burst limitu Azure AI Foundry
    time.sleep(0.5)

    # 3. RAG Retrieval
    rb_title, rb_content = retrieve_relevant_runbook(clean_snippet)

    # 4. Sub-Agent 2: Remediation
    remed_data, p_tok2, c_tok2 = run_remediation_agent(triage_data, clean_snippet, rb_title, rb_content)
    total_prompt_tokens += p_tok2
    total_completion_tokens += c_tok2

    # Malá pauza proti 429 burst limitu Azure AI Foundry
    time.sleep(0.5)

    # 5. Sub-Agent 3: Safety & Policy Auditor
    safety_data, p_tok3, c_tok3 = run_safety_agent(triage_data, remed_data)
    total_prompt_tokens += p_tok3
    total_completion_tokens += c_tok3

    # LLMOps kalkulace
    latency = round(time.time() - start_time, 2)
    total_tokens = total_prompt_tokens + total_completion_tokens
    cost_usd = round((total_prompt_tokens * 0.00000015) + (total_completion_tokens * 0.00000060), 6)

    summary = (
        f"{triage_data.get('clean_summary')} "
        f"[Použit runbook: {rb_title}]. "
        f"Komentář auditora: {safety_data.get('audit_comment')}"
    )

    model_info = f"{AZURE_AI_DEPLOYMENT_NAME} Multi-Agent (3x Sub-Agents) + RAG"

    return AuditResult(
        summary=summary,
        compliance_score=safety_data.get("compliance_score", 50),
        severity=triage_data.get("severity", "MEDIUM"),
        findings=remed_data.get("findings", []),
        remediated_snippet=remed_data.get("remediated_snippet", "# Beze změny"),
        model_used=model_info,
        latency_seconds=latency,
        prompt_tokens=total_prompt_tokens,
        completion_tokens=total_completion_tokens,
        total_tokens=total_tokens,
        cost_usd=cost_usd
    )
