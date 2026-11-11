import glob
import os
from typing import List, Tuple

RUNBOOKS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "data", "runbooks"
)

def load_all_runbooks() -> List[Tuple[str, str]]:
    """Načte všechny runbooky ze složky data/runbooks."""
    runbooks = []
    files = glob.glob(os.path.join(RUNBOOKS_DIR, "*.md"))
    for file_path in files:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            title = os.path.basename(file_path)
            runbooks.append((title, content))
    return runbooks

def retrieve_relevant_runbook(query_text: str) -> Tuple[str, str]:
    """RAG Retriever: Vyhledá nejrelevantnější NOTIX runbook pro daný log nebo kód."""
    runbooks = load_all_runbooks()
    if not runbooks:
        return "None", "Nebyl nalezen žádný specifický interní runbook."

    query_lower = query_text.lower()
    best_match = None
    best_score = -1

    for title, content in runbooks:
        score = 0
        content_lower = content.lower()

        keywords = [
            "auth.cms.gov.cz",
            "security-gateway",
            "timeout",
            "webclient",
            "privileged",
            "runasuser",
            "0.0.0.0/0",
            "ingress",
        ]
        for kw in keywords:
            if kw in query_lower and kw in content_lower:
                score += 3

        words = set(query_lower.split())
        for w in words:
            if len(w) > 4 and w in content_lower:
                score += 1

        if score > best_score:
            best_score = score
            best_match = (title, content)

    if best_match and best_score > 0:
        return best_match
    return "Generic", "Uplatňují se standardní globální SRE pravidla."
