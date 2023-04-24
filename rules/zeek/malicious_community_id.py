from typing import Any, List

def rule(event: Any) -> bool:

    community_id = event.get("community_id", None)

    if community_id is None:
        return False
    
    malicious_community_id: List[str] = [
        "1:zzttZJWjCAcZn3zZBNyZQ+/KesI="
    ]

    return community_id in malicious_community_id


