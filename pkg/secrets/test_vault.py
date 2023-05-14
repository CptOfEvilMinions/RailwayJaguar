from pkg.secrets.vault import GetSecret
from mock import patch


def test_GetSecret():
    test_secret = "super_secret"
    with patch("requests.get") as mock_request:
        mock_request.return_value.status_code = 200
        mock_request.return_value.text = test_secret
        status_code, resp = GetSecret("vault.example", "abc123", "test")

    assert isinstance(status_code, int)
    assert isinstance(resp, str)
    assert status_code == 200
    assert resp == test_secret


def test_NegativeGetSecret():
    with patch("requests.get") as mock_request:
        mock_request.return_value.status_code = 400
        mock_request.return_value.text = "Could not retrieve secret"
        status_code, resp = GetSecret("vault.example", "abc123", "test")

    assert isinstance(status_code, int)
    assert isinstance(resp, str)
    assert status_code == 400
    assert resp == "Could not retrieve secret"
