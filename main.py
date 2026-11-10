import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

endpoint = os.getenv("AZURE_AI_ENDPOINT")
api_key = os.getenv("AZURE_AI_API_KEY")

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(api_key),
)

response = client.complete(
    messages=[
        SystemMessage(content="Si enterprise SRE asistent."),
        UserMessage(content="Skontroluj konfiguráciu.")
    ],
    model="gpt-4.1-nano"
)

print(response.choices[0].message.content)
