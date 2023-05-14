from typing import Dict
import requests


def GetSecret(vault_addr: str, vault_token: str, secret_path: str) -> tuple[int, str]:
    """
    Retrieves a secret from Hashicorp Vault secrets manager

    Parameters:
        vault_token (str): Vault token used to authenticate
        secret_path (str): Secret to retrieve
    Returns:
        (str): Return secret in cleartext
    """
    headers: Dict[str, str] = {
        "X-Vault-Token": vault_token,
    }
    r = requests.get(
        url=f"https://{vault_addr}/v1/secret/{secret_path}",
        headers=headers,
    )
    return r.status_code, r.text
