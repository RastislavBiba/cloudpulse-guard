# scripts/provision_foundry_agents.py
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.agents import AgentsClient

load_dotenv()

PROJECT_ENDPOINT = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
MODEL_DEPLOYMENT = os.getenv("AZURE_AI_DEPLOYMENT_NAME", "gpt-5-mini")

if not PROJECT_ENDPOINT:
    raise ValueError("Chybí AZURE_AI_PROJECT_ENDPOINT v .env souboru!")

print(f"🔗 Připojuji k Azure AI Agent Service: {PROJECT_ENDPOINT}")
print(f"🤖 Model Deployment: {MODEL_DEPLOYMENT}")

# Vytvoření dedikovaného Agents klienta
agents_client = AgentsClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential()
)

print("\n🚀 Začínám registraci agentů v Azure AI Foundry...")

# 1. Triage Agent
print("\n[1/3] Vytvářím 'notix-triage-agent'...")
triage_agent = agents_client.create_agent(
    model=MODEL_DEPLOYMENT,
    name="notix-triage-agent",
    instructions="""Jsi Senior Triage Agent pro NOTIX SRE.
Tvým úkolem je rozebrat vstupní incident log nebo infrastrukturní kód a vrátit VÝHRADNĚ validní JSON v češtině:
{
  "severity": "CRITICAL" | "HIGH" | "MEDIUM" | "LOW",
  "component": "Název komponenty",
  "stack_category": "Kategorie stacku",
  "clean_summary": "Stručný a přesný popis incidentu v češtině"
}"""
)
print(f"✅ Triage Agent vytvořen! ID: {triage_agent.id}")

# 2. Remediation Agent
print("\n[2/3] Vytvářím 'notix-remediation-agent'...")
remed_agent = agents_client.create_agent(
    model=MODEL_DEPLOYMENT,
    name="notix-remediation-agent",
    instructions="""Jsi Senior Remediation SRE Inženýr pro NOTIX.
Na základě poskytnutého runbooku a triage kontextu navrhni opravený kód nebo diagnostické CLI příkazy.
Vrať VÝHRADNĚ validní JSON v češtině:
{
  "findings": [
    {
      "severity": "CRITICAL" | "HIGH" | "MEDIUM" | "LOW",
      "issue": "Název a popis problému",
      "recommendation": "Doporučený postup nápravy dle interního runbooku"
    }
  ],
  "remediated_snippet": "Opravený kód nebo diagnostické CLI"
}"""
)
print(f"✅ Remediation Agent vytvořen! ID: {remed_agent.id}")

# 3. Safety Agent
print("\n[3/3] Vytvářím 'notix-safety-agent'...")
safety_agent = agents_client.create_agent(
    model=MODEL_DEPLOYMENT,
    name="notix-safety-agent",
    instructions="""Jsi Nezávislý Bezpečnostní a Policy Auditor pro NOTIX systémy.
Zkontroluj navrženou opravu, ověř zda neobsahuje destruktivní příkazy a vypočítej finální compliance skóre (0 až 100).
Vrať VÝHRADNĚ validní JSON v češtině:
{
  "compliance_score": 0 az 100,
  "safety_verdict": "SCHVÁLENO" | "VYŽADUJE_SCHVÁLENÍ" | "ZAMÍTNUTO",
  "audit_comment": "Komentář auditora k bezpečnosti navrženého řešení v češtině"
}"""
)
print(f"✅ Safety Agent vytvořen! ID: {safety_agent.id}")

print("\n" + "=" * 55)
print("🎉 VŠICHNI 3 AGENTI BYLI ÚSPĚŠNĚ ZAREGISTROVÁNI V CLOUDU!")
print("=" * 55)
print("Zkopíruj si tato vygenerovaná ID a vlož je do svého souboru .env:\n")
print(f'AZURE_AGENT_TRIAGE_ID="{triage_agent.id}"')
print(f'AZURE_AGENT_REMEDIATION_ID="{remed_agent.id}"')
print(f'AZURE_AGENT_SAFETY_ID="{safety_agent.id}"')
