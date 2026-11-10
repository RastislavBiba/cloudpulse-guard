import os
from dotenv import load_dotenv

load_dotenv()

AZURE_AI_ENDPOINT = os.getenv("AZURE_AI_ENDPOINT")
AZURE_AI_API_KEY = os.getenv("AZURE_AI_API_KEY")
AZURE_AI_DEPLOYMENT_NAME = os.getenv("AZURE_AI_DEPLOYMENT_NAME", "gpt-4.1-nano")

if not AZURE_AI_ENDPOINT or not AZURE_AI_API_KEY:
    print("⚠️ VAROVANIE: AZURE_AI_ENDPOINT alebo AZURE_AI_API_KEY chýbajú v .env!")
