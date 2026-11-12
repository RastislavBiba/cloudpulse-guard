import os
import time
from azure.identity import DefaultAzureCredential
from azure.ai.agents import AgentsClient

_agents_client = None

def get_agents_client() -> AgentsClient:
    global _agents_client
    if _agents_client is None:
        endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
        if not endpoint:
            raise ValueError("AZURE_AI_PROJECT_ENDPOINT chýba v .env!")
        _agents_client = AgentsClient(
            endpoint=endpoint,
            credential=DefaultAzureCredential()
        )
    return _agents_client

def execute_agent_run(agent_id: str, prompt: str) -> tuple[str, int, int]:
    client = get_agents_client()

    thread = client.threads.create()

    client.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt
    )

    run = client.runs.create(
        thread_id=thread.id,
        agent_id=agent_id
    )

    max_wait = 45
    waited = 0
    while run.status in ["queued", "in_progress", "requires_action"]:
        time.sleep(1.0)
        waited += 1
        run = client.runs.get(thread_id=thread.id, run_id=run.id)
        if waited >= max_wait:
            break

    if run.status == "failed":
        err_msg = getattr(run, "last_error", "Neznáma chyba")
        raise RuntimeError(f"Agent {agent_id} zlyhal: {err_msg}")

    messages = client.messages.list(thread_id=thread.id)
    raw_text = ""
    for msg in messages:
        if msg.role == "assistant":
            for block in msg.content:
                if hasattr(block, "text") and hasattr(block.text, "value"):
                    raw_text += block.text.value
            if raw_text:
                break

    p_tok = getattr(run.usage, "prompt_tokens", 0) if hasattr(run, "usage") and run.usage else 0
    c_tok = getattr(run.usage, "completion_tokens", 0) if hasattr(run, "usage") and run.usage else 0

    return raw_text, p_tok, c_tok
