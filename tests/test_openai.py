import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

endpoint = os.getenv("AZURE_AI_ENDPOINT")
api_key = os.getenv("AZURE_AI_API_KEY")
deployment = os.getenv("AZURE_AI_DEPLOYMENT_NAME", "gpt-4.1-nano")

# Ak endpoint končí na /models alebo /openai/v1/responses, upravíme základnú URL
base_endpoint = endpoint.split("/openai")[0].split("/models")[0]

print(f"Pripájam sa na: {base_endpoint}")
print(f"Deployment name: {deployment}")

client = AzureOpenAI(
    azure_endpoint=base_endpoint,
    api_key=api_key,
    api_version="2024-06-01"  # overená stabilná verzia
)

try:
    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": "Si SRE DevOps expert."},
            {"role": "user", "content": "Ahoj, overujem spojenie z PyCharmu."}
        ]
    )
    print("✅ Úspešné spojenie!")
    print("Odpoveď:", response.choices[0].message.content)
    print(f"Spotrebované tokeny: {response.usage.total_tokens}")
except Exception as e:
    print("❌ Chyba:", str(e))
