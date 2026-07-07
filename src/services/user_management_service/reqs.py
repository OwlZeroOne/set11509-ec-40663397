import requests

SECURITY_URL = "http://password-service:5001/security"


def secure_password(password: str) -> str:
    return requests.post(
        f"{SECURITY_URL}/secure",
        json = {"password": password}
    ).json()["hashed"]