# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

AZURE_AI_ENDPOINT = os.getenv("AZURE_AI_ENDPOINT")
AZURE_AI_API_KEY = os.getenv("AZURE_AI_API_KEY")
AZURE_AI_DEPLOYMENT_NAME = os.getenv("AZURE_AI_DEPLOYMENT_NAME", "gpt-5-mini")

# Azure AI Agent Service konfigurace
AZURE_AI_PROJECT_ENDPOINT = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
AZURE_AGENT_TRIAGE_ID = os.getenv("AZURE_AGENT_TRIAGE_ID")
AZURE_AGENT_REMEDIATION_ID = os.getenv("AZURE_AGENT_REMEDIATION_ID")
AZURE_AGENT_SAFETY_ID = os.getenv("AZURE_AGENT_SAFETY_ID")
