from typing import Any, List

__MALICIOUS_COMMUNITY_IDS: List[str] = ["1:dpKcgnJE5EkTgO41o0aqUuf/MIQ="]


def rule(event: Any) -> bool:
    """
    Raise an alert when a Zeek conn event
    contains on of thee malicious community
    IDs defined above
    """

    community_id = event.get("community_id", None)

    if community_id is None:
        return False

    return community_id in __MALICIOUS_COMMUNITY_IDS
