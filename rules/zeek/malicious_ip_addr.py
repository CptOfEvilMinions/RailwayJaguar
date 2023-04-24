from typing import Any, List

def rule(event: Any) -> bool:

    ip_addr = event.get("id.resp_h", None)

    if ip_addr is None:
        return False
    
    malicious_ip_addrs: List[str] = [
        "91.189.92.38"
    ]

    return ip_addr in malicious_ip_addrs


