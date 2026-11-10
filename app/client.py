# app/client.py
from openai import OpenAI
from app.config import AZURE_AI_ENDPOINT, AZURE_AI_API_KEY


def get_azure_client() -> OpenAI:
    if not AZURE_AI_ENDPOINT or not AZURE_AI_API_KEY:
        raise ValueError("Chýbajú prístupové údaje pre Azure AI Foundry v .env!")

    return OpenAI(
        base_url=AZURE_AI_ENDPOINT,
        api_key=AZURE_AI_API_KEY,
    )
