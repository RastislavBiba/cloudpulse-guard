# app/agents_client.py
import time
import logging
from azure.identity import DefaultAzureCredential
from azure.ai.agents import AgentsClient
from app.config import AZURE_AI_PROJECT_ENDPOINT

logger = logging.getLogger("azure-agents")
_agents_client = None


def get_agents_client() -> AgentsClient:
    global _agents_client
    if _agents_client is None:
        if not AZURE_AI_PROJECT_ENDPOINT:
            raise ValueError("AZURE_AI_PROJECT_ENDPOINT není nastaven v .env")
        _agents_client = AgentsClient(
            endpoint=AZURE_AI_PROJECT_ENDPOINT,
            credential=DefaultAzureCredential()
        )
    return _agents_client


def execute_agent_run(agent_id: str, prompt: str) -> tuple[str, int, int]:
    """
    Spustí úlohu pre konkrétneho cloudového agenta v Azure AI Agent Service.
    Vráti: (odpoveď_text, prompt_tokens, completion_tokens)
    """
    client = get_agents_client()

    # 1. Vytvorenie cloudového vlákna (Thread)
    thread = client.threads.create()

    # 2. Vloženie správy do vlákna
    client.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt
    )

    # 3. Spustenie behu agenta
    run = client.runs.create(
        thread_id=thread.id,
        agent_id=agent_id
    )

    # 4. Čakanie na dokončenie (Polling)
    max_wait = 45
    waited = 0
    while run.status in ["queued", "in_progress", "requires_action"]:
        time.sleep(1.0)
        waited += 1
        run = client.runs.get(thread_id=thread.id, run_id=run.id)
        if waited >= max_wait:
            raise TimeoutError(f"Agent {agent_id} prekročil časový limit {max_wait}s.")

    # Ak beh zlyhal, vytiahneme presný dôvod z last_error
    if run.status != "completed":
        err_msg = "Neznáma chyba"
        if hasattr(run, "last_error") and run.last_error:
            err_msg = f"Kód: {getattr(run.last_error, 'code', 'N/A')}, Správa: {getattr(run.last_error, 'message', 'N/A')}"
        logger.error(f"Agent {agent_id} zlyhal: stav={run.status}, detail={err_msg}")
        raise RuntimeError(f"Agent beh selhal se stavem: {run.status}. Dôvod: {err_msg}")

    # 5. Vytiahnutie výslednej odpovede
    messages = client.messages.list(thread_id=thread.id)
    raw_response = ""
    for msg in messages:
        if msg.role == "assistant":
            for block in msg.content:
                if hasattr(block, "text") and hasattr(block.text, "value"):
                    raw_response += block.text.value
            break

    # 6. Spotreba tokenov
    p_tok = getattr(run.usage, "prompt_tokens", 0) if hasattr(run, "usage") and run.usage else 0
    c_tok = getattr(run.usage, "completion_tokens", 0) if hasattr(run, "usage") and run.usage else 0

    return raw_response, p_tok, c_tok
