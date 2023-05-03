from typing import Any, List


def rule(event: Any) -> bool:

    query = event.get("query", None)
    if query is None:
        return False

    malicious_dns: List[str] = ["hammerjs.github.io"]

    return query in malicious_dns
