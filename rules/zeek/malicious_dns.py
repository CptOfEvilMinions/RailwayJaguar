from typing import Any, List

__MALICIOUS_DOMAINS: List[str] = ["hammerjs.github.io"]


def rule(event: Any) -> bool:
    query = event.get("query", "UNKNOWN")
    return any(query.endswith(domain) for domain in __MALICIOUS_DOMAINS)
