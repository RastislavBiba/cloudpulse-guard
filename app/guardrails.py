import re
from typing import Tuple

SECRET_PATTERNS = [
    (r"(?i)(password|passwd|pwd|secret|token|api[_-]?key)\s*[:=]\s*['\"]?([^'\"\s]+)['\"]?", r"\1: [REDACTED_SECRET]"),
    (r"ghp_[A-Za-z0-9_]{36}", "[REDACTED_GITHUB_TOKEN]"),
    (r"ey[A-Za-z0-9_-]{10,}\.[A-Za-z0-9._-]{10,}", "[REDACTED_JWT_TOKEN]"),
    (r"-----BEGIN (RSA|OPENSSH|EC|DSA) PRIVATE KEY-----[\s\S]*?-----END \1 PRIVATE KEY-----", "[REDACTED_PRIVATE_KEY]"),
]

INJECTION_PATTERNS = [
    r"(?i)ignore\s+(all\s+)?(previous|prior)\s+instructions",
    r"(?i)disregard\s+the\s+system\s+prompt",
    r"(?i)you\s+are\s+now\s+(an\s+unrestricted|in\s+developer\s+mode)",
]

def sanitize_and_check_guardrails(input_text: str) -> Tuple[str, str, bool]:
    """
    Ověří vstup dle pravidel Content Safety:
    - Odhalí Prompt Injection
    - Maskuje hesla a tokeny
    Vrací: (sanitizovany_text, status_zprava, is_blocked)
    """
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, input_text):
            return input_text, "BLOKOVÁNO: Detekován pokus o Prompt Injection / Jailbreak.", True

    sanitized_text = input_text
    redacted = False
    for pattern, replacement in SECRET_PATTERNS:
        if re.search(pattern, sanitized_text):
            sanitized_text = re.sub(pattern, replacement, sanitized_text)
            redacted = True

    status = "SANITIZOVÁNO: Citlivé údaje byly automaticky začerněny." if redacted else "SCHVÁLENO: Vstup je bezpečný."
    return sanitized_text, status, False
