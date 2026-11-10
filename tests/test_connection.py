# test_connection.py
from app.client import get_azure_client
from app.config import AZURE_AI_DEPLOYMENT_NAME


def main():
    print(f"Pripájam sa na Azure AI Foundry model: {AZURE_AI_DEPLOYMENT_NAME}...")
    try:
        client = get_azure_client()

        # Vyskúšame štandardné chat completions, ktoré sú ideálne pre štruktúrovaných agentov
        try:
            response = client.chat.completions.create(
                model=AZURE_AI_DEPLOYMENT_NAME,
                messages=[
                    {"role": "system", "content": "Si špičkový Cloud & DevOps SRE auditor."},
                    {"role": "user", "content": "Ahoj, overujem spojenie z PyCharmu."}
                ]
            )
            print("✅ Úspešné spojenie cez Chat Completions!")
            print("Odpoveď:", response.choices[0].message.content)
            if hasattr(response, "usage") and response.usage:
                print(f"Tokeny: Input={response.usage.prompt_tokens}, Output={response.usage.completion_tokens}")
        except Exception as chat_err:
            print(f"Chat completions neprešli ({chat_err}), skúšam Responses API...")
            resp = client.responses.create(
                model=AZURE_AI_DEPLOYMENT_NAME,
                input="Ahoj, overujem spojenie z PyCharmu cez Responses API.",
            )
            print("✅ Úspešné spojenie cez Responses API!")
            print("Odpoveď:", resp.output)

    except Exception as e:
        print("❌ Chyba pri volaní Azure AI Foundry:", str(e))


if __name__ == "__main__":
    main()
