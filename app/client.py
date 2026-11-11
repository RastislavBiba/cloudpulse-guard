# app/client.py
from openai import OpenAI
from app.config import AZURE_AI_ENDPOINT, AZURE_AI_API_KEY

_azure_client = None

def get_azure_client() -> OpenAI:
    global _azure_client
    if _azure_client is None:
        _azure_client = OpenAI(
            base_url=AZURE_AI_ENDPOINT,
            api_key=AZURE_AI_API_KEY,
            max_retries=5,  # Automaticky počká a zkusí znovu při 429 Rate Limit
            timeout=30.0
        )
    return _azure_client
